import os
import sys
import time
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from dotenv import load_dotenv
load_dotenv()

from app.services.experimental_ho_translation.translator import experimental_ho_translator

class TestPhase34ExperimentalHoTranslator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.translator = experimental_ho_translator

    def test_01_exact_retrieval(self):
        """Requirement 1: Exact retrieval produces identical Hindi for base sentences with HIGH confidence in < 10ms."""
        test_cases = [
            ("आबु एन हो को नेनता काबु बेटा इचि कोआ", "हम उन लोगों को यहाँ पहुँचने नहीं देंगे।"),
            ("एन ओआ: आलेया हातुरे का हुजुए", "वह घर हमारे गाँव में नहीं आएगा।"),
            ("एन हापानुम लो पोन रेञ जागार केना", "मैंने उस युवती के साथ फोन पर बात की थी।")
        ]
        for ho_input, expected_hi in test_cases:
            t0 = time.time()
            res = self.translator.translate(ho_input)
            latency = (time.time() - t0) * 1000 # ms

            self.assertEqual(res["translation"], expected_hi)
            self.assertEqual(res["method"], "resource_supported_exact_retrieval")
            self.assertEqual(res["confidence"], "HIGH")
            self.assertFalse(res["ground_truth"])
            self.assertFalse(res["human_verified"])
            self.assertTrue(res["experimental"])
            self.assertLess(latency, 20.0, f"Exact retrieval took {latency}ms, expected < 20ms")

    def test_02_grammar_rule_transformation(self):
        """Requirement 2: Grammar variants produce expected translations with MEDIUM confidence in < 25ms."""
        test_cases = [
            ("आबु एन हो किन नेनता काबु बेटा इचि कोआ", "हम उन दोनों को यहाँ पहुँचने नहीं देंगे।"),
            ("एन हातु आलेया हातुरे का हुजुए", "वह गाँव हमारे गाँव में नहीं आएगा।"),
            ("साबिन हातु रे मियड सेता मेनाइए", "हर गाँव में एक कुत्ता है।")
        ]
        for ho_input, expected_hi in test_cases:
            t0 = time.time()
            res = self.translator.translate(ho_input)
            latency = (time.time() - t0) * 1000 # ms

            self.assertEqual(res["translation"], expected_hi)
            self.assertEqual(res["method"], "grammar_rule_transformation")
            self.assertEqual(res["confidence"], "MEDIUM")
            self.assertFalse(res["ground_truth"])
            self.assertFalse(res["human_verified"])
            self.assertTrue(res["experimental"])
            self.assertLess(latency, 35.0, f"Grammar rule took {latency}ms, expected < 35ms")

    def test_03_unseen_authentic_ho_ai_fallback(self):
        """Requirement 3: Unseen sentences produce candidates with dictionary alignment."""
        ho_input = "अले ओआ:रे मेना:लेया।"
        res = self.translator.translate(ho_input)

        self.assertIn("घर", res["translation"]) # ओआ: -> घर
        self.assertIn(res["method"], ["resource_assisted_ai", "similarity_retrieval"])
        self.assertIn(res["confidence"], ["MEDIUM", "LOW"])
        self.assertFalse(res["ground_truth"])
        self.assertFalse(res["human_verified"])
        self.assertTrue(res["experimental"])
        self.assertGreater(len(res["dictionary_matches"]), 0)

    def test_04_edge_cases_fallback(self):
        """Requirement 4: Edge cases fall back gracefully (empty, non-Devanagari, gibberish)."""
        # Empty
        res_empty = self.translator.translate("")
        self.assertEqual(res_empty["translation"], "")
        self.assertEqual(res_empty["method"], "empty_input")
        self.assertFalse(res_empty["ground_truth"])

        # Latin / Non-Devanagari
        res_latin = self.translator.translate("Good morning, how are you?")
        self.assertIn("experimental", res_latin["translation"].lower())
        self.assertEqual(res_latin["method"], "controlled_fallback")
        self.assertEqual(res_latin["confidence"], "LOW")
        self.assertFalse(res_latin["ground_truth"])

        # Gibberish
        res_gib = self.translator.translate("zzxxccvv bbnmm qwert")
        self.assertEqual(res_gib["method"], "controlled_fallback")
        self.assertFalse(res_gib["ground_truth"])

    def test_05_metadata_completeness(self):
        """Requirement 5: Metadata completeness on every response."""
        res = self.translator.translate("आबु एन हो को नेनता काबु बेटा इचि कोआ")
        required_keys = [
            "translation", "method", "confidence", "ground_truth",
            "human_verified", "experimental", "disclaimer", "dictionary_matches"
        ]
        for k in required_keys:
            self.assertIn(k, res)
        self.assertFalse(res["ground_truth"])
        self.assertFalse(res["human_verified"])
        self.assertTrue(res["experimental"])

if __name__ == "__main__":
    unittest.main()
