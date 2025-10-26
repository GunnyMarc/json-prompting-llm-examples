"""
Module: assemblyai/multichannel_transcription.py
Description: Multichannel audio transcription using AssemblyAI with structured output

This example demonstrates how to transcribe multichannel audio (e.g., phone calls
with separate channels for each speaker) with structured JSON output.

Usage:
    python assemblyai/multichannel_transcription.py

Requirements:
    - ASSEMBLYAI_API_KEY in environment variables
    - Python 3.9+
    - Multichannel audio file URL or local file path
"""

import os
import json
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

try:
    import assemblyai as aai
except ImportError:
    print("AssemblyAI package not installed. Install with: pip install assemblyai")
    exit(1)

load_dotenv()


class MultichannelTranscriber:
    """Transcribe multichannel audio with structured JSON output."""

    def __init__(self):
        """Initialize AssemblyAI client."""
        api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not api_key:
            raise ValueError("ASSEMBLYAI_API_KEY not found in environment variables")
        aai.settings.api_key = api_key

    def transcribe_multichannel(
        self,
        audio_url: str,
        enable_sentiment: bool = True,
        enable_entity_detection: bool = True
    ) -> Dict[str, Any]:
        """
        Transcribe multichannel audio (e.g., stereo phone call).

        Args:
            audio_url: URL or local path to audio file
            enable_sentiment: Enable sentiment analysis
            enable_entity_detection: Enable entity detection

        Returns:
            Dictionary with structured transcription per channel
        """
        # Configure transcription for multichannel
        config = aai.TranscriptionConfig(
            multichannel=True,
            sentiment_analysis=enable_sentiment,
            entity_detection=enable_entity_detection
        )

        # Create transcriber and process audio
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url, config)

        # Structure the output as JSON
        result = self._format_multichannel_json(transcript)
        return result

    def _format_multichannel_json(self, transcript) -> Dict[str, Any]:
        """
        Format multichannel transcript into structured JSON.

        Args:
            transcript: AssemblyAI transcript object

        Returns:
            Dictionary with structured multichannel transcript data
        """
        # Group words by channel
        channels = {}
        if transcript.words:
            for word in transcript.words:
                channel = word.channel
                if channel not in channels:
                    channels[channel] = {
                        "words": [],
                        "text": "",
                        "word_count": 0,
                        "duration_ms": 0
                    }

                channels[channel]["words"].append({
                    "text": word.text,
                    "start": word.start,
                    "end": word.end,
                    "confidence": word.confidence
                })

        # Build full text per channel
        for channel, data in channels.items():
            data["text"] = " ".join(w["text"] for w in data["words"])
            data["word_count"] = len(data["words"])
            if data["words"]:
                data["duration_ms"] = data["words"][-1]["end"] - data["words"][0]["start"]

        # Extract sentiment per channel if available
        channel_sentiments = {}
        if hasattr(transcript, 'sentiment_analysis_results') and transcript.sentiment_analysis_results:
            for sentiment in transcript.sentiment_analysis_results:
                channel = getattr(sentiment, 'channel', 'A')
                if channel not in channel_sentiments:
                    channel_sentiments[channel] = []

                channel_sentiments[channel].append({
                    "text": sentiment.text,
                    "sentiment": sentiment.sentiment,
                    "confidence": sentiment.confidence,
                    "start": sentiment.start,
                    "end": sentiment.end
                })

        # Extract entities per channel if available
        channel_entities = {}
        if hasattr(transcript, 'entities') and transcript.entities:
            for entity in transcript.entities:
                channel = getattr(entity, 'channel', 'A')
                if channel not in channel_entities:
                    channel_entities[channel] = []

                channel_entities[channel].append({
                    "text": entity.text,
                    "entity_type": entity.entity_type,
                    "start": entity.start,
                    "end": entity.end
                })

        # Build comprehensive result
        result = {
            "metadata": {
                "audio_duration_ms": transcript.audio_duration if hasattr(transcript, 'audio_duration') else None,
                "num_channels": len(channels),
                "total_words": sum(c["word_count"] for c in channels.values()),
                "language": transcript.language_code if hasattr(transcript, 'language_code') else None,
                "confidence_average": transcript.confidence if hasattr(transcript, 'confidence') else None
            },
            "full_transcript": transcript.text,
            "channels": {
                channel: {
                    "transcript": data["text"],
                    "word_count": data["word_count"],
                    "duration_ms": data["duration_ms"],
                    "duration_seconds": data["duration_ms"] / 1000 if data["duration_ms"] else 0,
                    "words": data["words"],
                    "sentiments": channel_sentiments.get(channel, []),
                    "entities": channel_entities.get(channel, []),
                    "sentiment_summary": self._summarize_sentiments(channel_sentiments.get(channel, []))
                }
                for channel, data in channels.items()
            },
            "channel_comparison": self._compare_channels(channels, channel_sentiments),
            "conversation_analysis": self._analyze_multichannel_conversation(channels)
        }

        return result

    def _summarize_sentiments(self, sentiments: List[Dict]) -> Dict[str, Any]:
        """Summarize sentiment analysis for a channel."""
        if not sentiments:
            return {
                "overall": "neutral",
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0
            }

        sentiment_counts = {
            "POSITIVE": 0,
            "NEGATIVE": 0,
            "NEUTRAL": 0
        }

        for s in sentiments:
            sentiment_counts[s["sentiment"]] += 1

        # Determine overall sentiment
        max_sentiment = max(sentiment_counts.items(), key=lambda x: x[1])

        return {
            "overall": max_sentiment[0].lower(),
            "positive_count": sentiment_counts["POSITIVE"],
            "negative_count": sentiment_counts["NEGATIVE"],
            "neutral_count": sentiment_counts["NEUTRAL"],
            "total_segments": len(sentiments)
        }

    def _compare_channels(
        self,
        channels: Dict[str, Any],
        sentiments: Dict[str, List[Dict]]
    ) -> Dict[str, Any]:
        """Compare statistics between channels."""
        comparison = {
            "word_count_by_channel": {},
            "speaking_time_by_channel": {},
            "dominant_channel": None,
            "balance_ratio": 0.0
        }

        # Word counts
        for channel, data in channels.items():
            comparison["word_count_by_channel"][channel] = data["word_count"]
            comparison["speaking_time_by_channel"][channel] = {
                "duration_ms": data["duration_ms"],
                "duration_seconds": data["duration_ms"] / 1000 if data["duration_ms"] else 0
            }

        # Determine dominant speaker
        if channels:
            dominant = max(channels.items(), key=lambda x: x[1]["word_count"])
            comparison["dominant_channel"] = dominant[0]

            # Calculate balance ratio (closer to 1.0 = more balanced)
            word_counts = [c["word_count"] for c in channels.values()]
            if len(word_counts) == 2 and max(word_counts) > 0:
                comparison["balance_ratio"] = min(word_counts) / max(word_counts)

        return comparison

    def _analyze_multichannel_conversation(self, channels: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the conversation dynamics across channels."""
        if not channels:
            return {}

        analysis = {
            "conversation_type": "",
            "interaction_level": "",
            "notes": []
        }

        # Determine conversation type based on channel balance
        if len(channels) == 2:
            word_counts = [c["word_count"] for c in channels.values()]
            ratio = min(word_counts) / max(word_counts) if max(word_counts) > 0 else 0

            if ratio > 0.7:
                analysis["conversation_type"] = "dialogue"
                analysis["interaction_level"] = "balanced"
                analysis["notes"].append("Both speakers contribute roughly equally")
            elif ratio > 0.4:
                analysis["conversation_type"] = "interview"
                analysis["interaction_level"] = "moderate"
                analysis["notes"].append("One speaker is more dominant")
            else:
                analysis["conversation_type"] = "monologue"
                analysis["interaction_level"] = "low"
                analysis["notes"].append("One speaker dominates the conversation")

        return analysis


def demo_multichannel_transcription():
    """Demonstrate multichannel transcription."""
    print("=" * 80)
    print("AssemblyAI Multichannel Transcription Example")
    print("=" * 80)
    print()

    # Sample multichannel audio URL (replace with your own)
    # This should be a stereo/multichannel audio file
    audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

    print(f"Processing audio: {audio_url}")
    print("This may take a minute...\n")

    try:
        transcriber = MultichannelTranscriber()
        result = transcriber.transcribe_multichannel(audio_url)

        print("-" * 80)
        print("\nTRANSCRIPT METADATA:")
        print(json.dumps(result["metadata"], indent=2))

        print("\n" + "-" * 80)
        print("\nCHANNEL COMPARISON:")
        print(json.dumps(result["channel_comparison"], indent=2))

        print("\n" + "-" * 80)
        print("\nCONVERSATION ANALYSIS:")
        print(json.dumps(result["conversation_analysis"], indent=2))

        print("\n" + "-" * 80)
        print("\nPER-CHANNEL TRANSCRIPTS:")
        for channel, data in result["channels"].items():
            print(f"\nChannel {channel}:")
            print(f"  Words: {data['word_count']}")
            print(f"  Duration: {data['duration_seconds']:.2f}s")
            print(f"  Sentiment: {data['sentiment_summary']}")
            print(f"  Transcript preview: {data['transcript'][:150]}...")

        # Save full result to file
        output_file = "multichannel_result.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\n" + "=" * 80)
        print(f"Full structured output saved to: {output_file}")
        print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        print("\nCommon issues:")
        print("1. Invalid ASSEMBLYAI_API_KEY")
        print("2. Audio file is not multichannel")
        print("3. Audio file URL not accessible")
        print("4. Network connectivity issues")


def main():
    """Main execution function."""
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        print("Error: ASSEMBLYAI_API_KEY not found in environment variables")
        print("Get your API key at: https://www.assemblyai.com/")
        print("Then add it to your .env file")
        return

    print("Multichannel Transcription with Structured JSON Output\n")
    print("Benefits of JSON structure for multichannel audio:")
    print("  ✓ Separate transcripts per channel")
    print("  ✓ Per-channel sentiment analysis")
    print("  ✓ Speaker balance metrics")
    print("  ✓ Conversation dynamics analysis")
    print("  ✓ Channel-specific entity extraction")
    print()

    demo_multichannel_transcription()

    print("\nUse Cases:")
    print("  • Phone call transcription and analysis")
    print("  • Customer service quality monitoring")
    print("  • Sales call analysis")
    print("  • Podcast/interview with separate mics")
    print("  • Legal call recordings")
    print("  • Support ticket audio analysis")
    print()


if __name__ == "__main__":
    main()
