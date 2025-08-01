# Testing Guide for Academic Source Credibility Checker

## Overview

The `test_agent_system.py` script provides comprehensive automated testing for the Academic Source Credibility Checker. It evaluates functionality, accuracy, robustness, and performance across multiple test scenarios.

## Quick Start

```bash
# Run all automated tests
python test_agent_system.py
```

## Test Cases

### 1. Normal Query Test
- **Query**: "Impact of AI on education"
- **Validates**: Basic functionality, result count, content summaries
- **Expected**: At least 3 credible sources with proper summaries

### 2. Low Credibility Query Test
- **Query**: "Clickbait AI News"
- **Validates**: Credibility scoring accuracy, source ranking
- **Expected**: Results ranked appropriately by credibility

### 3. Empty Query Test
- **Query**: Empty string
- **Validates**: Error handling and graceful failure
- **Expected**: Graceful failure or no results

### 4. Niche Query Test
- **Query**: "Quantum AI in goat farming"
- **Validates**: Handling of queries with few available sources
- **Expected**: Few or no results, graceful handling

### 5. Direct Credibility Scorer Test
- **Validates**: Domain-based scoring accuracy
- **Tests**: .edu, .com, academic publishers, blog platforms
- **Expected**: Appropriate scores for each domain type

### 6. Performance Benchmark
- **Query**: "machine learning algorithms"
- **Validates**: Response time and system performance
- **Expected**: Completion within 30 seconds

## Test Output

The script generates:

1. **Real-time Progress**: Shows each test execution with status updates
2. **Summary Table**: Formatted table with results for all tests
3. **JSON Log**: Detailed results saved to `test_results.json`

## Example Output

```
🚀 Running automated tests for Academic Source Credibility Checker...

[Test 1] Normal query: Impact of AI on education
  ✅ Research Agent found 5 sources
  ✅ Analysis Agent completed content summarization
  ✅ Credibility scoring and ranking completed
  Time taken: 15.2s

[Test 2] Known low credibility query: Clickbait AI News
  ✅ Found 4 sources and ranked appropriately
  ✅ Credibility scoring handled low-quality sources correctly
  Time taken: 12.8s

📊 TEST SUMMARY
┌─────────────────────────────────┬──────────┬──────────────────┬─────────────────┬─────────┬────────┐
│ Query                           │ #Results │ Top Domain       │ Credibility OK? │ Time(s) │ Passed │
├─────────────────────────────────┼──────────┼──────────────────┼─────────────────┼─────────┼────────┤
│ Impact of AI on education       │        5 │ mit.edu          │ ✅              │    15.2 │ ✅     │
│ Clickbait AI News               │        4 │ nature.com       │ ✅              │    12.8 │ ✅     │
│ Empty query                     │        0 │ -                │ ✅              │     0.1 │ ✅     │
│ Quantum AI in goat farming      │        1 │ arxiv.org        │ ✅              │     8.3 │ ✅     │
│ Credibility Scorer Direct Test  │        4 │ Multiple domains │ ✅              │     0.2 │ ✅     │
│ machine learning algorithms     │        6 │ ieee.org         │ ✅              │    14.7 │ ✅     │
└─────────────────────────────────┴──────────┴──────────────────┴─────────────────┴─────────┴────────┘

📈 Results: 6/6 tests passed
🎉 All tests passed!
⏱️ Average execution time: 8.6s
💾 Test results saved to test_results.json
```

## Prerequisites

1. **Environment Setup**: Ensure `.env` file contains valid `OPENAI_API_KEY`
2. **Dependencies**: All required packages installed (see main project requirements)
3. **Internet Connection**: Required for web scraping and API calls

## Understanding Test Results

### Validation Criteria

- **Result Count**: Normal queries should return 3+ sources
- **Credibility Scores**: Must be between 0-3.0 and properly sorted
- **Content Quality**: Summaries must be non-empty and meaningful
- **Performance**: Queries should complete within 30 seconds
- **Error Handling**: System should gracefully handle edge cases

### Common Issues and Solutions

**"OPENAI_API_KEY not found"**
- Check your `.env` file is properly configured
- Verify the API key is valid and has sufficient credits

**Tests timing out**
- Check internet connection
- Verify OpenAI API is accessible
- Some corporate networks may block certain requests

**Inconsistent results**
- Web scraping results can vary due to website availability
- Search results may change over time
- This is normal behavior for a real-world system

## Customizing Tests

You can modify `test_agent_system.py` to:

1. **Add new test queries**: Extend the test methods with additional scenarios
2. **Adjust validation criteria**: Modify the validation functions for different standards
3. **Change performance thresholds**: Update timing expectations based on your requirements
4. **Add domain-specific tests**: Include tests for specific academic fields

## Continuous Testing

For ongoing development, consider:

1. **Running tests before deployment**: Ensure system reliability
2. **Monitoring performance trends**: Track execution times over multiple runs
3. **Validating after changes**: Run tests after code modifications
4. **Periodic validation**: Ensure system maintains accuracy over time

## Integration with CI/CD

The test script returns appropriate exit codes:
- **0**: All tests passed
- **1**: Some tests failed or system error

This makes it suitable for integration with continuous integration pipelines.