"""
Module: assemblyai/speaker_diarization.py
Description: Speaker diarization example using AssemblyAI with structured JSON output

This example demonstrates how to use AssemblyAI's speaker diarization feature
to identify and label different speakers in audio, with structured JSON output.

Usage:
    python assemblyai/speaker_diarization.py

Requirements:
    - ASSEMBLYAI_API_KEY in environment variables
    - Python 3.9+
    - Audio file URL or local file path
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


class SpeakerDiarization:
    """Perform speaker diarization with structured JSON output."""

    def __init__(self):
        """Initialize AssemblyAI client."""
        api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not api_key:
            raise ValueError("ASSEMBLYAI_API_KEY not found in environment variables")
        aai.settings.api_key = api_key

    def transcribe_with_speakers(
        self,
        audio_url: str,
        speakers_expected: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio with speaker identification.

        Args:
            audio_url: URL or local path to audio file
            speakers_expected: Expected number of speakers (optional)

        Returns:
            Dictionary with structured transcription and speaker data
        """
        # Configure transcription with speaker diarization
        config = aai.TranscriptionConfig(
            speaker_labels=True,
            speakers_expected=speakers_expected
        )

        # Create transcriber and process audio
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url, config)

        # Structure the output as JSON
        result = self._format_transcript_json(transcript)
        return result

    def _format_transcript_json(self, transcript) -> Dict[str, Any]:
        """
        Format AssemblyAI transcript into structured JSON.

        Args:
            transcript: AssemblyAI transcript object

        Returns:
            Dictionary with structured transcript data
        """
        # Extract speaker segments
        speaker_segments = []
        if transcript.utterances:
            for utterance in transcript.utterances:
                speaker_segments.append({
                    "speaker": utterance.speaker,
                    "text": utterance.text,
                    "start_time": utterance.start,
                    "end_time": utterance.end,
                    "duration_ms": utterance.end - utterance.start,
                    "confidence": utterance.confidence
                })

        # Analyze speaker statistics
        speaker_stats = self._calculate_speaker_stats(speaker_segments)

        # Create full transcript by speaker
        speaker_transcripts = self._group_by_speaker(speaker_segments)

        # Build structured result
        result = {
            "metadata": {
                "audio_duration_ms": transcript.audio_duration if hasattr(transcript, 'audio_duration') else None,
                "language": transcript.language_code if hasattr(transcript, 'language_code') else None,
                "num_speakers_detected": len(speaker_stats),
                "total_words": transcript.words.__len__() if transcript.words else 0,
                "confidence_average": transcript.confidence if hasattr(transcript, 'confidence') else None
            },
            "full_transcript": transcript.text,
            "speaker_segments": speaker_segments,
            "speaker_statistics": speaker_stats,
            "speaker_transcripts": speaker_transcripts,
            "conversation_flow": self._analyze_conversation_flow(speaker_segments)
        }

        return result

    def _calculate_speaker_stats(self, segments: List[Dict]) -> Dict[str, Any]:
        """Calculate statistics for each speaker."""
        stats = {}

        for segment in segments:
            speaker = segment["speaker"]

            if speaker not in stats:
                stats[speaker] = {
                    "total_duration_ms": 0,
                    "num_segments": 0,
                    "word_count": 0,
                    "avg_confidence": []
                }

            stats[speaker]["total_duration_ms"] += segment["duration_ms"]
            stats[speaker]["num_segments"] += 1
            stats[speaker]["word_count"] += len(segment["text"].split())
            stats[speaker]["avg_confidence"].append(segment["confidence"])

        # Calculate averages and percentages
        total_duration = sum(s["total_duration_ms"] for s in stats.values())

        for speaker, data in stats.items():
            data["avg_confidence"] = sum(data["avg_confidence"]) / len(data["avg_confidence"])
            data["speaking_time_percentage"] = (data["total_duration_ms"] / total_duration * 100) if total_duration > 0 else 0
            data["avg_segment_duration_ms"] = data["total_duration_ms"] / data["num_segments"]
            data["total_duration_seconds"] = data["total_duration_ms"] / 1000

        return stats

    def _group_by_speaker(self, segments: List[Dict]) -> Dict[str, str]:
        """Group all text by speaker."""
        speaker_texts = {}

        for segment in segments:
            speaker = segment["speaker"]
            if speaker not in speaker_texts:
                speaker_texts[speaker] = []
            speaker_texts[speaker].append(segment["text"])

        return {
            speaker: " ".join(texts)
            for speaker, texts in speaker_texts.items()
        }

    def _analyze_conversation_flow(self, segments: List[Dict]) -> Dict[str, Any]:
        """Analyze the flow of conversation."""
        if not segments:
            return {}

        speaker_order = [seg["speaker"] for seg in segments]
        speaker_changes = sum(
            1 for i in range(1, len(speaker_order))
            if speaker_order[i] != speaker_order[i-1]
        )

        # Find longest uninterrupted segments
        longest_segments = sorted(
            segments,
            key=lambda x: x["duration_ms"],
            reverse=True
        )[:3]

        return {
            "total_speaker_changes": speaker_changes,
            "avg_segment_duration_ms": sum(s["duration_ms"] for s in segments) / len(segments),
            "conversation_style": self._determine_conversation_style(speaker_changes, len(segments)),
            "longest_uninterrupted_segments": [
                {
                    "speaker": seg["speaker"],
                    "duration_seconds": seg["duration_ms"] / 1000,
                    "preview": seg["text"][:100] + "..." if len(seg["text"]) > 100 else seg["text"]
                }
                for seg in longest_segments
            ]
        }

    def _determine_conversation_style(self, changes: int, total_segments: int) -> str:
        """Determine the style of conversation based on speaker changes."""
        if total_segments == 0:
            return "unknown"

        change_ratio = changes / total_segments

        if change_ratio > 0.7:
            return "highly_interactive"
        elif change_ratio > 0.4:
            return "conversational"
        elif change_ratio > 0.2:
            return "interview_style"
        else:
            return "monologue_style"


def demo_speaker_diarization():
    """Demonstrate speaker diarization with sample audio."""
    print("=" * 80)
    print("AssemblyAI Speaker Diarization Example")
    print("=" * 80)
    print()

    # Sample audio URL (replace with your own)
    # This is a public sample audio with multiple speakers
    audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

    print(f"Processing audio: {audio_url}")
    print("This may take a minute...\n")

    try:
        diarizer = SpeakerDiarization()
        result = diarizer.transcribe_with_speakers(audio_url, speakers_expected=2)

        print("-" * 80)
        print("\nTRANSCRIPT METADATA:")
        print(json.dumps(result["metadata"], indent=2))

        print("\n" + "-" * 80)
        print("\nSPEAKER STATISTICS:")
        print(json.dumps(result["speaker_statistics"], indent=2))

        print("\n" + "-" * 80)
        print("\nCONVERSATION FLOW ANALYSIS:")
        print(json.dumps(result["conversation_flow"], indent=2))

        print("\n" + "-" * 80)
        print("\nFIRST 5 SPEAKER SEGMENTS:")
        for segment in result["speaker_segments"][:5]:
            print(f"\n[{segment['speaker']}] ({segment['start_time']}ms - {segment['end_time']}ms)")
            print(f"  {segment['text']}")

        print("\n" + "-" * 80)
        print("\nFULL TRANSCRIPT BY SPEAKER:")
        for speaker, text in result["speaker_transcripts"].items():
            print(f"\n{speaker}:")
            print(f"  {text[:200]}..." if len(text) > 200 else f"  {text}")

        # Save full result to file
        output_file = "diarization_result.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\n" + "=" * 80)
        print(f"Full structured output saved to: {output_file}")
        print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        print("\nCommon issues:")
        print("1. Invalid ASSEMBLYAI_API_KEY")
        print("2. Audio file URL not accessible")
        print("3. Network connectivity issues")


def main():
    """Main execution function."""
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        print("Error: ASSEMBLYAI_API_KEY not found in environment variables")
        print("Get your API key at: https://www.assemblyai.com/")
        print("Then add it to your .env file")
        return

    print("Speaker Diarization with Structured JSON Output\n")
    print("Benefits of JSON structure for speaker diarization:")
    print("  ✓ Easy speaker identification and tracking")
    print("  ✓ Precise timestamp information")
    print("  ✓ Speaker statistics and analytics")
    print("  ✓ Conversation flow analysis")
    print("  ✓ Integration-ready format")
    print()

    demo_speaker_diarization()

    print("\nUse Cases:")
    print("  • Meeting transcription and analysis")
    print("  • Podcast episode summaries")
    print("  • Interview transcription")
    print("  • Customer service call analysis")
    print("  • Focus group research")
    print("  • Legal depositions")
    print()


if __name__ == "__main__":
    main()
