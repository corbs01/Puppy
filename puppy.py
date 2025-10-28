import os
import platform
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

file_path = Path(__file__).with_name("Molly_Training_Guide.pdf")
assets_dir = file_path.with_name("assets")
assets_dir.mkdir(exist_ok=True)

PALETTE = {
    "ink": HexColor("#1C2A39"),
    "muted_green": HexColor("#628A7A"),
    "powder_blue": HexColor("#E1F3F7"),
    "soft_teal": HexColor("#A9D6CF"),
    "sage": HexColor("#CFE6DA"),
    "beige": HexColor("#F7F1EB"),
    "navy": HexColor("#2B3A42"),
    "sand": HexColor("#F2DFCE"),
    "accent": HexColor("#F4B860"),
}


def ensure_image(url: str, filename: str) -> Optional[Path]:
    """Download background image if missing; return local path or None on failure."""
    destination = assets_dir / filename
    if destination.exists():
        return destination
    try:
        urllib.request.urlretrieve(url, destination)
        return destination
    except Exception:
        return None


# Curated Unsplash backgrounds (free to use) — will download once.
BACKGROUND_SOURCES = [
    (
        "https://images.unsplash.com/photo-1525253086316-d0c936c814f8?auto=format&fit=crop&w=1920&q=80",
        "slide01.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1508672019048-805c876b67e2?auto=format&fit=crop&w=1920&q=80",
        "slide02.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1552058544-f2b08422138a?auto=format&fit=crop&w=1920&q=80",
        "slide03.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1596496052190-1ff5c1c8d402?auto=format&fit=crop&w=1920&q=80",
        "slide04.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1522276498395-f4f68f7f8458?auto=format&fit=crop&w=1920&q=80",
        "slide05.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1601758066074-8c505b2ab540?auto=format&fit=crop&w=1920&q=80",
        "slide06.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=1920&q=80",
        "slide07.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1548199973-4b7ef27452ec?auto=format&fit=crop&w=1920&q=80",
        "slide08.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1525253086316-52962fb8212f?auto=format&fit=crop&w=1920&q=80",
        "slide09.jpg",
    ),
    (
        "https://images.unsplash.com/photo-1619983081573-430f63602796?auto=format&fit=crop&w=1920&q=80",
        "slide10.jpg",
    ),
]

BACKGROUND_IMAGES = [ensure_image(url, name) for url, name in BACKGROUND_SOURCES]

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleStyle",
        fontSize=40,
        leading=42,
        spaceAfter=16,
        textColor=PALETTE["ink"],
        alignment=1,
        tracking=1,
    )
)
styles.add(
    ParagraphStyle(
        name="SubtitleStyle",
        parent=styles["BodyText"],
        fontSize=20,
        leading=24,
        textColor=PALETTE["muted_green"],
        spaceAfter=20,
        alignment=1,
        tracking=0.6,
    )
)
styles.add(
    ParagraphStyle(
        name="SlideHeading",
        parent=styles["BodyText"],
        fontSize=26,
        leading=30,
        textColor=PALETTE["ink"],
        spaceAfter=10,
        tracking=1,
    )
)
styles.add(
    ParagraphStyle(
        name="SlideSubtitle",
        parent=styles["BodyText"],
        fontSize=18,
        leading=22,
        textColor=PALETTE["muted_green"],
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCopy",
        parent=styles["BodyText"],
        fontSize=14,
        leading=20,
        textColor=PALETTE["ink"],
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletStyle",
        parent=styles["BodyText"],
        fontSize=15,
        leading=22,
        textColor=PALETTE["ink"],
        leftIndent=20,
        bulletIndent=10,
        bulletFontSize=11,
        bulletColor=PALETTE["accent"],
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutStyle",
        parent=styles["BodyText"],
        fontSize=15,
        leading=21,
        textColor=PALETTE["ink"],
        backColor=PALETTE["powder_blue"],
        borderColor=PALETTE["muted_green"],
        borderWidth=1.2,
        borderPadding=10,
        spaceBefore=10,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="CardTitle",
        parent=styles["BodyText"],
        fontSize=13,
        leading=18,
        textColor=PALETTE["muted_green"],
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CardBody",
        parent=styles["BodyText"],
        fontSize=12,
        leading=17,
        textColor=PALETTE["ink"],
    )
)


def bullet(text: str) -> Paragraph:
    return Paragraph(f"<bullet>&#9679;</bullet>{text}", styles["BulletStyle"])


def callout(text: str) -> Paragraph:
    return Paragraph(text, styles["CalloutStyle"])


def card(title: str, body: str) -> Table:
    data = [
        [Paragraph(f"<b>{title}</b>", styles["CardTitle"])],
        [Paragraph(body, styles["CardBody"])],
    ]
    table = Table(data, colWidths=[360])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.Color(1, 1, 1, alpha=0.82)),
                ("BOX", (0, 0), (-1, -1), 1, colors.Color(0.7, 0.8, 0.75)),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return table


def pastel_table(data: List[List[str]], col_widths: List[int]) -> Table:
    table = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(1, 1, 1, alpha=0.75)),
                ("TEXTCOLOR", (0, 0), (-1, 0), PALETTE["ink"]),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.8, 0.86, 0.9)),
                ("BACKGROUND", (0, 1), (-1, -1), colors.Color(1, 1, 1, alpha=0.6)),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


# ---------------------------------------------------------------------------
# Slide content
# ---------------------------------------------------------------------------

@dataclass
class Slide:
    background: Optional[Path]
    elements: List


slides: List[Slide] = [
    Slide(
        background=BACKGROUND_IMAGES[0],
        elements=[
            Paragraph("Molly × Luna", styles["TitleStyle"]),
            Paragraph("Calm Companion Keynote Guide", styles["SubtitleStyle"]),
            Spacer(1, 20),
            callout(
                "World-class plan: raise a golden retriever who radiates confidence, adores her cat sister, "
                "and floats through the home with calm, Canva-worthy grace."
            ),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[1],
        elements=[
            Paragraph("Training Mindset", styles["SlideHeading"]),
            Paragraph("Short reps • generous rewards • end on a high note", styles["SlideSubtitle"]),
            bullet("1–3 minute micro-sessions, 3–5 times a day, layered between rest and play."),
            bullet("Reward early and often—happy brains learn cues in half the reps."),
            bullet("Use baby gates, tethers, and the x-pen like a backstage crew keeping the show seamless."),
            bullet("Capture wins in a shared note—patterns appear quickly when you track the glow-ups."),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[2],
        elements=[
            Paragraph("Studio Setup Checklist", styles["SlideHeading"]),
            bullet("42\" crate with divider, sleek x-pen, and two stylish baby gates to zone the space."),
            bullet("Chew gallery: stuffable rubber, long-lasting chew, velvet-soft chew for variety."),
            bullet("6-ft leash, flat collar, front-clip harness ready for the growth spurt."),
            bullet("Treat palette: pea-sized rewards or kibble for endless rapid-fire reps."),
            bullet("Luna’s lounge: elevated dining, gated litter spa, multiple escape catwalks."),
            callout("Night-before ritual: scent swap by trading soft cloths rubbed on each pet—instant familiarity."),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[3],
        elements=[
            Paragraph("First 48 Hours", styles["SlideHeading"]),
            Paragraph("Create the calm landing that Canva dreams are made of.", styles["SlideSubtitle"]),
            bullet("Stage one ‘base camp’ room with cozy textures and soft lighting."),
            bullet("Crate confetti: toss 5–10 treats, close the door for a gentle 5-count, reopen, repeat."),
            bullet("Potty autopilot: outdoors after naps, meals, play bursts, and every 45–60 minutes awake."),
            bullet("Scent-only meetups: swap spaces while one pet explores the other’s vibe solo."),
            card(
                "Pro Tip",
                "Play low-volume spa music and diffuse a pet-safe calming scent. It helps both Molly and Luna exhale.",
            ),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[4],
        elements=[
            Paragraph("Signature Day (Weeks 8–12)", styles["SlideHeading"]),
            pastel_table(
                [
                    ["Time", "Design of the Moment"],
                    ["06:30", "Potty, soft sunrise greeting, breakfast via puzzle feeder."],
                    ["07:00", "Name + sit mini-session, gentle play burst, potty reset."],
                    ["09:30", "Crate/x-pen nap behind a calm soundtrack."],
                    ["11:00", "Potty → recall game → cat-look & treat behind the gallery gate."],
                    ["12:30", "Lunch, potty, stuffed chew while you work nearby."],
                    ["15:00", "Potty → leave-it reps → mindful sniff walk on driveway or yard."],
                    ["18:00", "Dinner, potty, enrichment: find-it scatter, shaping trick, or snuffle mat."],
                    ["20:30", "Potty → settle-on-mat practice with dim lights."],
                    ["22:00", "Final potty → bedtime (expect 1–2 night breaks early on)."],
                ],
                [90, 420],
            ),
            callout("Movement guide: ~5 minutes of structured exercise per month of age, 2–3×/day, plus rich sniffing adventures."),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[5],
        elements=[
            Paragraph("Potty & Crate Wins", styles["SlideHeading"]),
            bullet("Supervision or soft confinement keeps rehearsal perfect—no free-roam until she’s nailing it."),
            bullet("Same potty runway every time; whisper the cue mid-go; celebrate within two seconds."),
            bullet("Accidents: gentle clap, straight outside, then enzymatic cleanup—no drama, all data."),
            bullet("Crate ladder: treat tosses → quick door closes → stuffed chew calm → fade your presence."),
            bullet("Alone-time arc: gated room → tiny departures → 15–30 min errands, building toward 60."),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[6],
        elements=[
            Paragraph("Skill Sessions", styles["SlideHeading"]),
            Paragraph("Micro-reps that feel like play.", styles["SlideSubtitle"]),
            bullet("Bite inhibition: rotate 2–3 legal chews daily; redirect nips instantly."),
            bullet("Timeouts: 30–60 sec behind a baby gate if mouthing persists (crate stays a zen den)."),
            bullet("Core cues: name sparkle, sit/down rhythms, hallway come ping-pong, leave-it ladder, drop trades, settle-on-mat bliss."),
            bullet("Greeting etiquette: pay four paws on the floor, cue sits, use leashes or x-pen for guest entrances."),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[7],
        elements=[
            Paragraph("Socialization Mood Board", styles["SlideHeading"]),
            bullet("1–2 fresh experiences daily—quit while she’s curious, not overwhelmed."),
            bullet("Pair every new human, surface, sound, or vehicle with soft treats and exit on a smile."),
            bullet("Secure car rides with a crate or crash-tested harness; rehearse vet-table handling with steady pay."),
            bullet("Leave before she asks to—confidence grows when sessions end on ‘I want more!’"),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[8],
        elements=[
            Paragraph("Cat × Puppy Blueprint", styles["SlideHeading"]),
            pastel_table(
                [
                    ["Phase", "Timing", "Signature Moves"],
                    ["Prep", "Before arrival", "Scent swap, feed across doors, curate cat-only sanctuaries."],
                    ["Parallel", "Days 1–3", "Separate lives; reward Molly for sniffing then checking back with you."],
                    ["See-But-Separate", "Days 3–7", "Barrier intros with Look-At-That. Sessions 1–3 minutes."],
                    ["Shared Space", "Week 2", "Molly on leash with chew; Luna controls distance; settle-on-mat practice."],
                    ["Drag-Line", "Weeks 3–4", "Light line indoors for quick resets; remove after 7–10 calm sessions."],
                    ["Everyday Harmony", "~8 weeks", "More open doors; cat-only zones stay sacred; reward random calm moments."],
                ],
                [90, 90, 330],
            ),
            callout("Feed & train Molly before cat sessions. Give Luna private play parties while Molly relaxes with a chew."),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[9],
        elements=[
            Paragraph("Milestone Roadmap", styles["SlideHeading"]),
            pastel_table(
                [
                    ["Timeline", "Celebrate This"],
                    ["Weeks 8–10", "Potty rhythm clicks, crate naps 30–60 min, barrier cat sessions feel easy."],
                    ["Weeks 10–12", "Leave-it/drop/settle flourish; Luna joins on-leash room hangs 5–10 min."],
                    ["Weeks 12–16", "Long-line recalls, vet handling readiness, alone-time up to an hour."],
                    ["4–6 Months", "Adolescence glow-up: richer rewards, refreshed boundaries, positive puppy class."],
                ],
                [120, 370],
            ),
            Paragraph("Common Hiccups", styles["SlideHeading"]),
            bullet("Laser focus on Luna? Add distance, boost treat value, rehearse settle-on-mat, pre-session sniff walk."),
            bullet("Cat swats or hisses? Give Luna a dog-free day, reset to barriers, elevate escape routes."),
            bullet("Potty regression? Tighten to a 45-minute timer, shrink roaming area for 3–5 days."),
            bullet("Night waking? Keep evenings zen, last potty right before lights out, quiet overnight escort, zero party vibes."),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[0],
        elements=[
            Paragraph("Safety Signals & Trainer Faves", styles["SlideHeading"]),
            bullet("Dog stress whispers: whale eye, lip lick outside treats, tight yawns, freezing, slow tail sweep."),
            bullet("Cat stress cues: pinned ears, tucked tail, dilated pupils, tail thumps, crouched stillness."),
            bullet("Spot stress? Dial back intensity, switch to easy wins, wrap with something joyful."),
            bullet("Teach: hand target redirect, go-to-mat parking cue, find-it scatter for instant decompression."),
            Paragraph("Daily & Weekly Rhythm", styles["SlideHeading"]),
            bullet("Daily: three micro-training snacks, two crate rests with chews, one to two enrichment feeders."),
            bullet("Weekly: one new calm location, one fresh surface or sound, one new person at Molly’s comfort distance."),
            bullet("Meals: three/day until ~12 weeks, then two. Funnel part into training paychecks."),
            bullet("Toolkit: crate + divider, x-pen, baby gates, flat collar, 6-ft leash, long line, front-clip harness, treat pouch, chew trio."),
        ],
    ),
    Slide(
        background=BACKGROUND_IMAGES[1],
        elements=[
            Paragraph("Wrap with Joy", styles["SlideHeading"]),
            callout(
                "Every calm glance, every polite pass-by, every shared nap is a slide-worthy win. "
                "Celebrate relentlessly—it cements the friendship you’re crafting."
            ),
            bullet("Keep notes on what lights Molly up and what soothes Luna."),
            bullet("When progress sticks, zoom out, simplify, and reboot with kindness."),
            bullet("You’ve got this—and I’m just a message away whenever you want to iterate."),
            Paragraph("— Your Calm Companion Coach", styles["SlideSubtitle"]),
        ],
    ),
]

# ---------------------------------------------------------------------------
# Document assembly
# ---------------------------------------------------------------------------

PAGE_SIZE = landscape(A4)
PAGE_WIDTH, PAGE_HEIGHT = PAGE_SIZE
CONTENT_FRAME = Frame(
    90,
    90,
    PAGE_WIDTH - 180,
    PAGE_HEIGHT - 180,
    showBoundary=0,
)


def make_on_page(background: Optional[Path]):
    def _on_page(canvas, doc):
        canvas.saveState()
        if background and background.exists():
            canvas.drawImage(
                str(background),
                0,
                0,
                width=PAGE_WIDTH,
                height=PAGE_HEIGHT,
                preserveAspectRatio=True,
                anchor="c",
            )
        else:
            canvas.setFillColor(PALETTE["beige"])
            canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)

        # Soft overlay for readability
        canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.6))
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)

        # Accent bar
        canvas.setFillColor(PALETTE["soft_teal"])
        canvas.rect(60, 60, PAGE_WIDTH - 120, 20, fill=True, stroke=False)

        # Footer
        canvas.setFont("Helvetica", 10)
        canvas.setFillColor(PALETTE["navy"])
        footer = f"Molly × Luna • Calm Companion Keynote • Slide {doc.page}"
        canvas.drawCentredString(PAGE_WIDTH / 2, 40, footer)
        canvas.restoreState()

    return _on_page


doc = BaseDocTemplate(
    str(file_path),
    pagesize=PAGE_SIZE,
    rightMargin=0,
    leftMargin=0,
    topMargin=0,
    bottomMargin=0,
)

templates = [
    PageTemplate(id=f"Slide{idx}", frames=[CONTENT_FRAME], onPage=make_on_page(slide.background))
    for idx, slide in enumerate(slides)
]
for template in templates:
    doc.addPageTemplates(template)

story: List = []
for idx, slide in enumerate(slides):
    if idx > 0:
        story.append(NextPageTemplate(f"Slide{idx}"))
        story.append(PageBreak())
    story.extend(slide.elements)

doc.build(story)


def open_pdf(path: Path) -> None:
    """Open the generated PDF with the default system viewer."""
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", str(path)], check=True)
    elif system == "Windows":
        os.startfile(str(path))  # type: ignore[attr-defined]
    else:
        subprocess.run(["xdg-open", str(path)], check=True)


if __name__ == "__main__":
    open_pdf(file_path)
