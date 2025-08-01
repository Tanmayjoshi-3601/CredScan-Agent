# Academic Source Credibility Checker

## Performance Optimization Guide

### Speed Optimization

The application has been optimized for faster performance:

1. **Parallel Processing**: Sources are processed in parallel using ThreadPoolExecutor
2. **Reduced Search Strategies**: Limited to 3 most effective search patterns
3. **Content Limiting**: Content is truncated to 1500 characters for faster processing
4. **Streamlined Flow**: Removed CrewAI delegation loops that caused delays

### GPU Usage

While this application doesn't directly use GPU acceleration, you can run it on GPU-enabled environments:

**For OpenAI API calls**: The OpenAI GPT-4o model runs on OpenAI's GPU infrastructure automatically.

**For local processing**: To enable GPU acceleration for potential future ML features:

1. **Install CUDA** (if using NVIDIA GPUs):
   ```bash
   # Check if CUDA is available
   nvidia-smi
   ```

2. **GPU-enabled libraries** (for future enhancements):
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Memory considerations**:
   - GPU memory is typically more limited than RAM
   - Current implementation is optimized for CPU/RAM usage
   - Web scraping and API calls don't benefit from GPU acceleration

### Performance Settings

Current optimizations:
- **Max sources**: Limited to 5 for faster processing
- **Parallel workers**: 3 threads for content processing
- **Content limit**: 1500 characters per source
- **Search strategies**: 3 optimized patterns

### Monitoring Performance

The application provides real-time status updates showing:
- Search progress
- Processing time per source
- Strategy effectiveness
- Error handling

### Deployment Considerations

For fastest performance:
1. **Use SSD storage** for faster file I/O
2. **Sufficient RAM** (2GB+ recommended)
3. **Good internet connection** for web scraping
4. **OpenAI API limits** may be the bottleneck for large queries