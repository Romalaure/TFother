package fr.timefield.tfother.tiplouf;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

/** Minimal client for the OpenAI chat completions, embeddings, transcription and speech endpoints. */
public final class OpenAiClient {
    private static final HttpClient HTTP = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build();

    private OpenAiClient() {
    }

    public static boolean isConfigured() {
        return !TiploufConfig.API_KEY.get().isBlank();
    }

    /** Sends the messages and returns the text of the answer. */
    public static CompletableFuture<String> chat(JsonArray messages) {
        JsonObject body = new JsonObject();
        body.addProperty("model", TiploufConfig.CHAT_MODEL.get());
        body.add("messages", messages);
        body.addProperty("max_completion_tokens", TiploufConfig.MAX_COMPLETION_TOKENS.get());
        String effort = TiploufConfig.REASONING_EFFORT.get();
        if (!effort.isBlank()) {
            body.addProperty("reasoning_effort", effort);
        }
        return post("/chat/completions", body, Duration.ofSeconds(60)).thenApply(json -> {
            JsonObject choice = json.getAsJsonArray("choices").get(0).getAsJsonObject();
            JsonElement content = choice.getAsJsonObject("message").get("content");
            if (content == null || content.isJsonNull() || content.getAsString().isBlank()) {
                throw new IllegalStateException("Empty answer (finish_reason=" + choice.get("finish_reason") + ")");
            }
            return content.getAsString();
        });
    }

    /** Returns one L2-normalized vector per input, in order. */
    public static CompletableFuture<float[][]> embed(List<String> inputs) {
        JsonObject body = new JsonObject();
        body.addProperty("model", TiploufConfig.EMBEDDING_MODEL.get());
        body.addProperty("dimensions", TiploufConfig.EMBEDDING_DIMENSIONS.get());
        JsonArray input = new JsonArray();
        inputs.forEach(input::add);
        body.add("input", input);
        return post("/embeddings", body, Duration.ofSeconds(120)).thenApply(json -> {
            float[][] vectors = new float[inputs.size()][];
            for (JsonElement e : json.getAsJsonArray("data")) {
                JsonObject item = e.getAsJsonObject();
                JsonArray values = item.getAsJsonArray("embedding");
                float[] v = new float[values.size()];
                for (int i = 0; i < v.length; i++) {
                    v[i] = values.get(i).getAsFloat();
                }
                vectors[item.get("index").getAsInt()] = normalize(v);
            }
            return vectors;
        });
    }

    /** Transcribes a WAV recording of French speech. {@code prompt} lists words the model should expect. */
    public static CompletableFuture<String> transcribe(byte[] wav, String prompt) {
        String boundary = "----tiplouf" + UUID.randomUUID().toString().replace("-", "");
        List<byte[]> parts = new ArrayList<>();
        for (String[] field : new String[][]{
                {"model", TiploufConfig.TRANSCRIPTION_MODEL.get()},
                {"language", "fr"},
                {"response_format", "json"},
                {"prompt", prompt}}) {
            parts.add(("--" + boundary + "\r\nContent-Disposition: form-data; name=\"" + field[0] + "\"\r\n\r\n"
                    + field[1] + "\r\n").getBytes(StandardCharsets.UTF_8));
        }
        parts.add(("--" + boundary + "\r\nContent-Disposition: form-data; name=\"file\"; filename=\"question.wav\"\r\n"
                + "Content-Type: audio/wav\r\n\r\n").getBytes(StandardCharsets.UTF_8));
        parts.add(wav);
        parts.add(("\r\n--" + boundary + "--\r\n").getBytes(StandardCharsets.UTF_8));
        return send("/audio/transcriptions", "multipart/form-data; boundary=" + boundary,
                HttpRequest.BodyPublishers.ofByteArrays(parts), Duration.ofSeconds(60))
                .thenApply(bytes -> JsonParser.parseString(new String(bytes, StandardCharsets.UTF_8))
                        .getAsJsonObject().get("text").getAsString().strip());
    }

    /** Reads the text aloud. Returns raw 24 kHz 16-bit little-endian mono PCM. */
    public static CompletableFuture<byte[]> speech(String text) {
        JsonObject body = new JsonObject();
        String model = TiploufConfig.SPEECH_MODEL.get();
        body.addProperty("model", model);
        body.addProperty("voice", TiploufConfig.SPEECH_VOICE.get());
        body.addProperty("input", text);
        body.addProperty("response_format", "pcm");
        String instructions = TiploufConfig.SPEECH_INSTRUCTIONS.get();
        // Only the gpt-4o TTS models accept instructions, tts-1 rejects them.
        if (model.startsWith("gpt-") && !instructions.isBlank()) {
            body.addProperty("instructions", instructions);
        }
        return send("/audio/speech", "application/json",
                HttpRequest.BodyPublishers.ofString(body.toString()), Duration.ofSeconds(60));
    }

    static float[] normalize(float[] v) {
        double norm = 0;
        for (float x : v) {
            norm += x * x;
        }
        float inv = norm == 0 ? 0 : (float) (1 / Math.sqrt(norm));
        for (int i = 0; i < v.length; i++) {
            v[i] *= inv;
        }
        return v;
    }

    private static CompletableFuture<JsonObject> post(String path, JsonObject body, Duration timeout) {
        return send(path, "application/json", HttpRequest.BodyPublishers.ofString(body.toString()), timeout)
                .thenApply(bytes -> JsonParser.parseString(new String(bytes, StandardCharsets.UTF_8)).getAsJsonObject());
    }

    private static CompletableFuture<byte[]> send(String path, String contentType, HttpRequest.BodyPublisher body,
                                                  Duration timeout) {
        String base = TiploufConfig.API_BASE_URL.get().replaceAll("/+$", "");
        HttpRequest request = HttpRequest.newBuilder(URI.create(base + path))
                .timeout(timeout)
                .header("Authorization", "Bearer " + TiploufConfig.API_KEY.get().trim())
                .header("Content-Type", contentType)
                .POST(body)
                .build();
        return HTTP.sendAsync(request, HttpResponse.BodyHandlers.ofByteArray()).thenApply(response -> {
            if (response.statusCode() / 100 != 2) {
                throw new ApiException(response.statusCode(), new String(response.body(), StandardCharsets.UTF_8));
            }
            return response.body();
        });
    }

    public static final class ApiException extends RuntimeException {
        public ApiException(int status, String body) {
            super("HTTP " + status + ": " + (body.length() > 500 ? body.substring(0, 500) + "..." : body));
        }
    }
}
