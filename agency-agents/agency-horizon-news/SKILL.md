# Horizon - AI Tech News Curator

**AI curates the tech news. You just read.**

Horizon collects news from multiple customizable sources, uses AI to score and filter them, and generates a daily briefing — complete with summaries, community discussions, and background explanations in both English and Chinese.

## Source

- **Repository**: https://github.com/Thysrael/Horizon
- **Live Demo**: https://thysrael.github.io/Horizon/
- **License**: MIT

## What It Does

Horizon is an automated tech news aggregator that:

1. **📡 Multi-Source Aggregation** — Collects from Hacker News, RSS feeds, Reddit, Telegram channels, and GitHub (releases & user events)
2. **🤖 AI-Powered Scoring** — Uses Claude, GPT-4, Gemini, DeepSeek, Doubao, or any OpenAI-compatible API to rate each item 0-10, filtering out the noise
3. **🌐 Bilingual Summaries** — Generates daily reports in both English and Chinese
4. **🔍 Content Enrichment** — Searches the web to provide background knowledge for unfamiliar concepts
5. **💬 Community Voices** — Collects and summarizes discussions from comments on HackerNews, Reddit, etc.
6. **🔗 Cross-Source Deduplication** — Merges duplicate items from different platforms automatically
7. **📧 Email Subscription** — Self-hosted newsletter system (SMTP/IMAP) that handles "Subscribe" requests automatically
8. **📝 Static Site Generation** — Deploys as a GitHub Pages site via GitHub Actions, updated on a schedule

## How It Works

```
              ┌──────────┐
              │ Hacker   │
┌─────────┐   │ News     │   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  RSS    │──▶│ Reddit   │──▶│ AI Score │──▶│ Enrich   │──▶│ Summary  │
│ Telegram│   │ GitHub   │   │ & Filter │   │ & Search │   │ & Deploy │
└─────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
  Fetch from      Merge &        Score          Web search     Generate
  all sources    deduplicate     0-10 each      background     Markdown &
                                & filter        knowledge      deploy site
```

## Installation

### Option A: Local Installation

```bash
git clone https://github.com/Thysrael/Horizon.git
cd horizon

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### Option B: Docker

```bash
git clone https://github.com/Thysrael/Horizon.git
cd horizon

# Copy and edit configuration
cp config/config.example.json config/config.json

# Run with docker-compose
docker-compose up -d
```

## Configuration

Edit `config/config.json`:

```json
{
  "ai": {
    "provider": "openai",
    "api_key": "your-api-key",
    "model": "gpt-4"
  },
  "sources": {
    "hackernews": true,
    "reddit": ["r/programming", "r/technology"],
    "rss": ["https://news.ycombinator.com/rss"],
    "telegram": ["@tech_channel"],
    "github": {
      "releases": ["owner/repo"],
      "events": ["username"]
    }
  },
  "filter": {
    "min_score": 6.0,
    "max_items": 20
  },
  "output": {
    "language": ["en", "zh"],
    "deploy": {
      "enabled": true,
      "target": "github_pages"
    }
  }
}
```

## Usage

### Run Once

```bash
# Using uv
uv run horizon

# Or using Python
python -m horizon
```

### Run on Schedule

The repository includes GitHub Actions workflows for automatic daily updates.

### Generate Report

```bash
# Generate today's report
horizon generate --date today

# Generate for specific date
horizon generate --date 2024-01-01

# Force regeneration
horizon generate --force
```

## Output Structure

```
output/
├── 2024/
│   ├── 01/
│   │   ├── 01.md          # Daily report in Markdown
│   │   ├── 01_en.md       # English version
│   │   └── 01_zh.md       # Chinese version
│   └── ...
└── index.html             # Static site homepage
```

## Features in Detail

### AI Scoring

Each news item is scored 0-10 based on:
- **Technical Depth** — How technical/in-depth is the content
- **Novelty** — How new/unique is the information
- **Impact** — Potential impact on the tech industry
- **Community Interest** — Engagement level from source platform

### Content Enrichment

For high-scoring items, Horizon:
1. Searches the web for background context
2. Summarizes community discussions
3. Extracts key technical concepts
4. Provides related resources

### Deduplication

Automatically merges items that:
- Point to the same URL
- Have similar titles (fuzzy matching)
- Cover the same topic from different sources

## Deployment

### GitHub Pages (Recommended)

1. Fork the repository
2. Enable GitHub Pages in settings
3. Configure GitHub Actions secrets:
   - `AI_API_KEY` — Your AI provider API key
4. The site auto-updates daily

### Self-Hosted

```bash
# Build static site
horizon build --output ./site

# Serve locally
horizon serve --port 8080
```

## API Integration

Supported AI providers:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- DeepSeek
- Doubao
- Any OpenAI-compatible API

## Customization

### Add New Sources

Edit `src/sources/` and implement:
```python
class CustomSource(BaseSource):
    async def fetch(self) -> List[NewsItem]:
        # Your implementation
        pass
```

### Custom Scoring

Modify `src/scoring/` to adjust how items are rated.

### Custom Output Format

Edit templates in `templates/` to change report format.

## Environment Variables

```bash
# AI Provider
AI_PROVIDER=openai
AI_API_KEY=your-api-key
AI_MODEL=gpt-4

# Optional: Proxy
HTTP_PROXY=http://proxy:8080
HTTPS_PROXY=http://proxy:8080

# Optional: Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-password
```

## Troubleshooting

### Common Issues

**Q: AI scoring is slow**
A: Enable parallel processing in config or use a faster model

**Q: Duplicate items still appear**
A: Adjust similarity threshold in deduplication settings

**Q: Deployment fails**
A: Check GitHub token permissions and repository settings

## Related Projects

- [Hacker News](https://news.ycombinator.com/)
- [Lobsters](https://lobste.rs/)
- [Techmeme](https://www.techmeme.com/)

## Contributing

See [CONTRIBUTING.md](https://github.com/Thysrael/Horizon/blob/main/CONTRIBUTING.md)

## License

MIT License - See [LICENSE](https://github.com/Thysrael/Horizon/blob/main/LICENSE)
