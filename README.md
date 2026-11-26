# parlayapi-obs-overlay

A single-file OBS browser source for rehearsing a sports broadcast and previewing a moneyline ticker. The rehearsal file rotates three fictional matchups locally. The feed preview requests available lines from ParlayAPI.

![Rehearsal ticker showing a fictional matchup between the Harbor Owls and Valley Foxes, with sample prices clearly labeled](docs/rehearsal.png)

## Rehearse a scene offline

1. [Download rehearsal.html](https://github.com/JacobiusMakes/parlayapi-obs-overlay/releases/download/rehearsal-v1.0/rehearsal.html). Open it in a browser to see the first matchup immediately.
2. In OBS, add a **Browser** source, select **Local file** and choose the downloaded file. Set the source to 1920 × 1080. The lower third has a transparent background.
3. Watch the Owls and Foxes rotate to the Kites and Lynx after eight seconds. **REHEARSAL** and **Fictional teams and prices** stay on screen as each matchup changes.

The downloadable rehearsal file works without an internet connection or account. To build it yourself, run `python3 build_rehearsal.py rehearsal.html` from this repository.

## Set up the feed preview

1. [Download the feed preview](https://github.com/JacobiusMakes/parlayapi-obs-overlay/raw/refs/heads/main/overlay.html) and save it as `overlay.html` on your machine.
2. In OBS: Sources, click +, choose Browser.
3. Leave "Local file" unchecked and put a `file:///` URL in the URL field so you can pass options:
   - Windows: `file:///C:/overlays/overlay.html?sport=nfl&theme=dark`
   - macOS: `file:///Users/you/overlays/overlay.html?sport=nfl&theme=dark`
4. Set Width 1920, Height 1080, FPS 30.
5. Recommended: check "Shutdown source when not visible" so the overlay stops polling while the scene is hidden.

The ticker renders as a lower third near the bottom of the 1920x1080 canvas. Move or scale the source like any other.

Tip: to preview outside OBS, open the same URL in a normal browser with `&bg=1` appended. That paints a dark test backdrop behind the transparent overlay. Do not use `bg=1` inside OBS.

## Customization (URL parameters)

| Param | Values | Default | What it does |
|---|---|---|---|
| `sport` | `nfl`, `nba`, `mlb`, `nhl`, `ncaaf`, `ncaab`, `wnba`, `epl`, or any full sport key | all sports | Filter the ticker to one sport |
| `theme` | `dark`, `light` | `dark` | Pill color scheme |
| `speed` | seconds, min 3 | `8` | How long each game stays on screen |
| `max` | 1 to 15 | `10` | How many games rotate |
| `bg` | `1` | off | Test backdrop for previewing outside OBS |
| `mode` | `rehearsal` | feed preview in `overlay.html` | Show fictional matchups offline. The dedicated rehearsal download always uses sample data. The sport filter applies to the feed preview. |

Example: `overlay.html?sport=nba&theme=light&speed=6&max=8`

## Why there is no API key parameter

On purpose. An API key pasted into an OBS browser source URL is visible in your source settings, in settings screen shares, and in "just checking my scenes" moments on stream. Leaked keys get abused and then rotated, which breaks your overlay mid-broadcast. This overlay only calls the keyless public surface, so there is nothing to leak. A `key` or `apiKey` param is ignored if you add one.

## What the feed preview shows

The preview requests the public board once per minute and shows the prices and bookmakers in its response. Coverage varies. A successful empty response clears the ticker. If a refresh fails while prices are on screen, the ticker labels them **Cached · refresh failed** until a later successful response.

Before displaying API-derived prices in a public broadcast, confirm the data-use permissions for your production. To plan for a particular sport, market and refresh interval, use the [ParlayAPI evaluation lab](https://parlay-api.com/tools/evaluation-lab?utm_source=github&utm_medium=broadcast_tool&utm_campaign=obs_scene_rehearsal).

## Compatibility notes

- Requires OBS 28 or newer (the built-in browser is modern Chromium). Older OBS versions with CEF from 2020 or earlier should also work but are untested.
- The feed preview requests `parlay-api.com/live/api/command_center` at startup and once per minute while open. Rehearsal mode makes zero network requests.
- Responsible gambling: this shows odds data, not betting advice. 21+, where legal.

## License

MIT. See [LICENSE](LICENSE).

---

Part of the [ParlayAPI](https://parlay-api.com) ecosystem: a real-time sports odds API with a free tier of 1,000 credits per month, no card required. Explore all the tools at [github.com/JacobiusMakes](https://github.com/JacobiusMakes).
