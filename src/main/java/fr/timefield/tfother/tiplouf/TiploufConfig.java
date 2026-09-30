package fr.timefield.tfother.tiplouf;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * Tiplouf settings, in config/tfother-tiplouf.toml.
 *
 * <p>COMMON config on purpose: SERVER configs are synced to clients, which would leak the API key.
 */
public final class TiploufConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.ConfigValue<String> API_KEY;
    public static final ModConfigSpec.ConfigValue<String> API_BASE_URL;
    public static final ModConfigSpec.ConfigValue<String> CHAT_MODEL;
    public static final ModConfigSpec.ConfigValue<String> REASONING_EFFORT;
    public static final ModConfigSpec.IntValue MAX_COMPLETION_TOKENS;
    public static final ModConfigSpec.ConfigValue<String> EMBEDDING_MODEL;
    public static final ModConfigSpec.IntValue EMBEDDING_DIMENSIONS;
    public static final ModConfigSpec.IntValue CONTEXT_CHUNKS;
    public static final ModConfigSpec.IntValue HISTORY_TURNS;
    public static final ModConfigSpec.IntValue CONVERSATION_TIMEOUT_SECONDS;
    public static final ModConfigSpec.IntValue COOLDOWN_SECONDS;
    public static final ModConfigSpec.IntValue DAILY_QUESTIONS_PER_PLAYER;
    public static final ModConfigSpec.BooleanValue VOICE_ENABLED;
    public static final ModConfigSpec.BooleanValue VOICE_PRIVATE;
    public static final ModConfigSpec.ConfigValue<String> TRANSCRIPTION_MODEL;
    public static final ModConfigSpec.ConfigValue<String> SPEECH_MODEL;
    public static final ModConfigSpec.ConfigValue<String> SPEECH_VOICE;
    public static final ModConfigSpec.ConfigValue<String> SPEECH_INSTRUCTIONS;

    static {
        ModConfigSpec.Builder b = new ModConfigSpec.Builder();

        b.push("api");
        API_KEY = b.comment("OpenAI API key (sk-...). Only needed on the server. Tiplouf stays silent while it is empty.")
                .define("apiKey", "");
        API_BASE_URL = b.comment("Base URL of an OpenAI-compatible API.")
                .define("baseUrl", "https://api.openai.com/v1");
        CHAT_MODEL = b.comment("Model that writes the answers.")
                .define("chatModel", "gpt-5-nano");
        REASONING_EFFORT = b.comment("reasoning_effort sent with each question (minimal, low, medium, high).",
                        "Leave empty for models without reasoning, such as gpt-4o-mini.")
                .define("reasoningEffort", "minimal");
        MAX_COMPLETION_TOKENS = b.comment("Answer size limit, reasoning tokens included.")
                .defineInRange("maxCompletionTokens", 1200, 100, 16000);
        EMBEDDING_MODEL = b.comment("Model used to search the knowledge base. Leave empty to use keyword search only.")
                .define("embeddingModel", "text-embedding-3-small");
        EMBEDDING_DIMENSIONS = b.comment("Size of the embedding vectors (lower = less memory).")
                .defineInRange("embeddingDimensions", 512, 64, 3072);
        b.pop();

        b.push("conversation");
        CONTEXT_CHUNKS = b.comment("Knowledge base extracts sent with each question.")
                .defineInRange("contextChunks", 6, 1, 20);
        HISTORY_TURNS = b.comment("Previous questions/answers Tiplouf remembers in a conversation.")
                .defineInRange("historyTurns", 3, 0, 10);
        CONVERSATION_TIMEOUT_SECONDS = b.comment("The conversation ends after this idle time.")
                .defineInRange("timeoutSeconds", 120, 10, 3600);
        COOLDOWN_SECONDS = b.comment("Minimum delay between two questions of the same player.")
                .defineInRange("cooldownSeconds", 3, 0, 600);
        DAILY_QUESTIONS_PER_PLAYER = b.comment("Questions per player per day (0 = unlimited).")
                .defineInRange("dailyQuestionsPerPlayer", 50, 0, 100000);
        b.pop();

        b.push("voice");
        VOICE_ENABLED = b.comment("With Simple Voice Chat installed, Tiplouf understands spoken questions (in French)",
                        "and reads his answers aloud to players who have the voice chat.")
                .define("enabled", true);
        VOICE_PRIVATE = b.comment("While a player talks with Tiplouf, their voice is not sent to the other players.")
                .define("privateVoice", true);
        TRANSCRIPTION_MODEL = b.comment("Speech-to-text model (gpt-4o-mini-transcribe, gpt-4o-transcribe, whisper-1).")
                .define("transcriptionModel", "gpt-4o-mini-transcribe");
        SPEECH_MODEL = b.comment("Text-to-speech model (gpt-4o-mini-tts, tts-1). Leave empty so Tiplouf does not speak.")
                .define("speechModel", "gpt-4o-mini-tts");
        SPEECH_VOICE = b.comment("Tiplouf's voice (alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer, verse).")
                .define("speechVoice", "fable");
        SPEECH_INSTRUCTIONS = b.comment("How Tiplouf speaks (gpt-4o-mini-tts only).")
                .define("speechInstructions", "Parle en français de France, avec une voix aiguë, enjouée et un peu "
                        + "fanfaronne de petit pingouin. Débit naturel et assez rapide.");
        b.pop();

        SPEC = b.build();
    }

    private TiploufConfig() {
    }
}
