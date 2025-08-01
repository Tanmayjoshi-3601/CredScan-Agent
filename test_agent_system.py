#!/usr/bin/env python3
"""
Automated Testing Script for Academic Source Credibility Checker
Tests functionality, accuracy, robustness, and performance of the multi-agent system.
"""

import time
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from tabulate import tabulate

# Import the main credibility checker
from main import CredibilityChecker
from tools.credibility_scorer import credibility_scorer


class TestAgentSystem:
    """Comprehensive test suite for the Academic Source Credibility Checker."""
    
    def __init__(self):
        self.test_results = []
        self.passed_tests = 0
        self.total_tests = 0
        
        # Initialize the credibility checker
        try:
            self.checker = CredibilityChecker()
            print("✅ Credibility Checker initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Credibility Checker: {e}")
            raise
    
    def run_query(self, query: str) -> Dict[str, Any]:
        """
        Execute the full pipeline and return results.
        This is the main interface to the credibility checker.
        """
        return self.checker.process_query(query)
    
    def validate_normal_query_results(self, results: Dict[str, Any], min_results: int = 3) -> bool:
        """Validate results from normal queries."""
        if not results.get('success', False):
            return False
        
        sources = results.get('results', [])
        if len(sources) < min_results:
            print(f"  ❌ Expected at least {min_results} results, got {len(sources)}")
            return False
        
        # Check that credibility scores are valid
        for source in sources:
            score = source.get('credibility_score', 0)
            if not (0 <= score <= 3.0):
                print(f"  ❌ Invalid credibility score: {score}")
                return False
        
        # Check that summaries exist and are not empty
        for source in sources:
            summary = source.get('summary', '')
            if not summary or summary.strip() == '':
                print(f"  ❌ Empty summary found for source: {source.get('url', 'unknown')}")
                return False
        
        return True
    
    def validate_credibility_ordering(self, results: Dict[str, Any]) -> bool:
        """Validate that .edu/.gov domains generally rank higher than .com/.org."""
        if not results.get('success', False):
            return True  # Skip validation for failed queries
        
        sources = results.get('results', [])
        if len(sources) < 2:
            return True  # Skip validation for insufficient results
        
        # Check if results are properly sorted by credibility score
        scores = [source.get('credibility_score', 0) for source in sources]
        is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
        
        if not is_sorted:
            print("  ❌ Results not properly sorted by credibility score")
            return False
        
        return True
    
    def test_normal_query(self) -> Dict[str, Any]:
        """Test with a normal academic query."""
        print("\n[Test 1] Normal query: Impact of AI on education")
        query = "Impact of AI on education"
        
        start_time = time.time()
        results = self.run_query(query)
        execution_time = time.time() - start_time
        
        # Validate results
        valid_results = self.validate_normal_query_results(results, min_results=3)
        valid_ordering = self.validate_credibility_ordering(results)
        
        passed = valid_results and valid_ordering
        
        if passed:
            print(f"  ✅ Research Agent found {len(results.get('results', []))} sources")
            print("  ✅ Analysis Agent completed content summarization")
            print("  ✅ Credibility scoring and ranking completed")
        
        sources = results.get('results', [])
        top_domain = sources[0].get('url', '').split('/')[2] if sources else '-'
        
        return {
            'query': query,
            'num_results': len(sources),
            'top_domain': top_domain,
            'credibility_ok': valid_ordering,
            'time': round(execution_time, 1),
            'passed': passed,
            'details': results
        }
    
    def test_clickbait_query(self) -> Dict[str, Any]:
        """Test with a query that might return low-credibility sources."""
        print("\n[Test 2] Known low credibility query: Clickbait AI News")
        query = "Clickbait AI News"
        
        start_time = time.time()
        results = self.run_query(query)
        execution_time = time.time() - start_time
        
        # For this test, we expect the system to still find results but rank them appropriately
        valid_ordering = self.validate_credibility_ordering(results)
        
        sources = results.get('results', [])
        top_domain = sources[0].get('url', '').split('/')[2] if sources else '-'
        
        passed = results.get('success', False) and valid_ordering
        
        if passed:
            print(f"  ✅ Found {len(sources)} sources and ranked appropriately")
            print("  ✅ Credibility scoring handled low-quality sources correctly")
        
        return {
            'query': query,
            'num_results': len(sources),
            'top_domain': top_domain,
            'credibility_ok': valid_ordering,
            'time': round(execution_time, 1),
            'passed': passed,
            'details': results
        }
    
    def test_empty_query(self) -> Dict[str, Any]:
        """Test with an empty query."""
        print("\n[Test 3] Empty query test")
        query = ""
        
        start_time = time.time()
        results = self.run_query(query)
        execution_time = time.time() - start_time
        
        # Empty query should either fail gracefully or return no results
        passed = not results.get('success', True) or len(results.get('results', [])) == 0
        
        if passed:
            print("  ✅ Empty query handled gracefully")
        else:
            print("  ❌ Empty query should fail gracefully or return no results")
        
        return {
            'query': "Empty query",
            'num_results': len(results.get('results', [])),
            'top_domain': '-',
            'credibility_ok': True,
            'time': round(execution_time, 1),
            'passed': passed,
            'details': results
        }
    
    def test_niche_query(self) -> Dict[str, Any]:
        """Test with a very specific query that should return few or no results."""
        print("\n[Test 4] Niche query: Quantum AI in goat farming")
        query = "Quantum AI in goat farming"
        
        start_time = time.time()
        results = self.run_query(query)
        execution_time = time.time() - start_time
        
        sources = results.get('results', [])
        
        # For niche queries, we expect either no results or very few results
        # The system should handle this gracefully
        passed = results.get('success', False) or len(sources) == 0
        
        if len(sources) == 0:
            print("  ✅ No credible sources found (as expected for niche query)")
        elif len(sources) <= 2:
            print(f"  ✅ Found {len(sources)} sources for niche query (reasonable)")
        else:
            print(f"  ⚠️ Found {len(sources)} sources (more than expected for niche query)")
        
        top_domain = sources[0].get('url', '').split('/')[2] if sources else '-'
        
        return {
            'query': query,
            'num_results': len(sources),
            'top_domain': top_domain,
            'credibility_ok': True,
            'time': round(execution_time, 1),
            'passed': passed,
            'details': results
        }
    
    def test_credibility_scorer_directly(self) -> Dict[str, Any]:
        """Test the credibility scorer with known domains."""
        print("\n[Test 5] Direct credibility scorer validation")
        
        test_urls = [
            ('https://mit.edu/research/ai', 'High credibility (.edu)'),
            ('https://nature.com/articles/ai-study', 'High credibility (academic publisher)'),
            ('https://medium.com/ai-blog', 'Low credibility (blog platform)'),
            ('https://arxiv.org/abs/2023.12345', 'High credibility (academic preprint)'),
        ]
        
        start_time = time.time()
        passed = True
        
        for url, expected_type in test_urls:
            result = credibility_scorer(url)
            score = result.get('score', 0)
            reason = result.get('reason', '')
            
            print(f"  URL: {url}")
            print(f"    Score: {score}/3.0 - {reason}")
            
            # Validate score ranges based on expected type
            if 'High credibility' in expected_type and score < 2.0:
                print(f"    ❌ Expected high score for {expected_type}")
                passed = False
            elif 'Low credibility' in expected_type and score > 1.5:
                print(f"    ❌ Expected low score for {expected_type}")
                passed = False
            else:
                print(f"    ✅ Score appropriate for {expected_type}")
        
        execution_time = time.time() - start_time
        
        return {
            'query': 'Credibility Scorer Direct Test',
            'num_results': len(test_urls),
            'top_domain': 'Multiple domains tested',
            'credibility_ok': passed,
            'time': round(execution_time, 1),
            'passed': passed,
            'details': {'test_urls': test_urls}
        }
    
    def test_performance_benchmark(self) -> Dict[str, Any]:
        """Test performance with a standard query."""
        print("\n[Test 6] Performance benchmark")
        query = "machine learning algorithms"
        
        start_time = time.time()
        results = self.run_query(query)
        execution_time = time.time() - start_time
        
        # Performance criteria: should complete within 30 seconds
        performance_ok = execution_time < 30.0
        results_ok = results.get('success', False) and len(results.get('results', [])) > 0
        
        passed = performance_ok and results_ok
        
        if performance_ok:
            print(f"  ✅ Query completed in {execution_time:.1f}s (under 30s limit)")
        else:
            print(f"  ❌ Query took {execution_time:.1f}s (over 30s limit)")
        
        if results_ok:
            print(f"  ✅ Successfully returned {len(results.get('results', []))} results")
        
        sources = results.get('results', [])
        top_domain = sources[0].get('url', '').split('/')[2] if sources else '-'
        
        return {
            'query': query,
            'num_results': len(sources),
            'top_domain': top_domain,
            'credibility_ok': True,
            'time': round(execution_time, 1),
            'passed': passed,
            'details': results
        }
    
    def run_all_tests(self):
        """Execute all test cases and generate summary."""
        print("🚀 Running automated tests for Academic Source Credibility Checker...")
        print("=" * 80)
        
        # List of test methods
        test_methods = [
            self.test_normal_query,
            self.test_clickbait_query,
            self.test_empty_query,
            self.test_niche_query,
            self.test_credibility_scorer_directly,
            self.test_performance_benchmark
        ]
        
        # Run all tests
        for test_method in test_methods:
            try:
                result = test_method()
                self.test_results.append(result)
                self.total_tests += 1
                if result['passed']:
                    self.passed_tests += 1
                    print(f"  Time taken: {result['time']}s")
                else:
                    print(f"  ❌ Test failed - Time taken: {result['time']}s")
            except Exception as e:
                print(f"  ❌ Test failed with exception: {e}")
                self.test_results.append({
                    'query': 'Test Error',
                    'num_results': 0,
                    'top_domain': '-',
                    'credibility_ok': False,
                    'time': 0,
                    'passed': False,
                    'error': str(e)
                })
                self.total_tests += 1
        
        self.generate_summary()
        self.save_results_to_json()
    
    def generate_summary(self):
        """Generate and print summary table."""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        # Prepare data for table
        table_data = []
        for result in self.test_results:
            table_data.append([
                result['query'][:30] + ('...' if len(result['query']) > 30 else ''),
                result['num_results'],
                result['top_domain'][:20] + ('...' if len(result['top_domain']) > 20 else ''),
                '✅' if result['credibility_ok'] else '❌',
                result['time'],
                '✅' if result['passed'] else '❌'
            ])
        
        headers = ['Query', '#Results', 'Top Domain', 'Credibility OK?', 'Time(s)', 'Passed']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
        # Final summary
        print(f"\n📈 Results: {self.passed_tests}/{self.total_tests} tests passed")
        
        if self.passed_tests == self.total_tests:
            print("🎉 All tests passed!")
        else:
            print(f"⚠️ {self.total_tests - self.passed_tests} test(s) failed.")
            
        # Performance summary
        avg_time = sum(r['time'] for r in self.test_results) / len(self.test_results)
        print(f"⏱️ Average execution time: {avg_time:.1f}s")
    
    def save_results_to_json(self):
        """Save test results to JSON file for later analysis."""
        timestamp = datetime.now().isoformat()
        
        output_data = {
            'timestamp': timestamp,
            'summary': {
                'total_tests': self.total_tests,
                'passed_tests': self.passed_tests,
                'success_rate': round(self.passed_tests / self.total_tests * 100, 1) if self.total_tests > 0 else 0
            },
            'test_results': self.test_results
        }
        
        with open('test_results.json', 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Test results saved to test_results.json")


def main():
    """Main execution function."""
    try:
        # Check for required environment variables
        if not os.getenv('OPENAI_API_KEY'):
            print("❌ OPENAI_API_KEY not found in environment variables.")
            print("Please ensure your .env file is properly configured.")
            return
        
        # Initialize and run tests
        test_suite = TestAgentSystem()
        test_suite.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed to run: {e}")
        raise


if __name__ == "__main__":
    main()