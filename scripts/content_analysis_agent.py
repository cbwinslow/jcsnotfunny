#!/usr/bin/env python3
"""
Content Analysis & Enhancement Agent
Analyzes video content and generates optimized cards, thumbnails, tags, and metadata
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class ThumbnailSpec:
    """Specification for thumbnail generation"""

    concept: str
    colors: List[str]
    text_overlay: str
    emotion: str
    viral_elements: List[str]


@dataclass
class ContentCard:
    """Content card for social media"""

    headline: str
    subheadline: str
    key_points: List[str]
    call_to_action: str
    hashtags: List[str]
    engagement_prompt: str


@dataclass
class VideoMetadata:
    """Complete video metadata package"""

    title: str
    description: str
    tags: List[str]
    category: str
    thumbnail_spec: ThumbnailSpec
    content_cards: List[ContentCard]
    upload_schedule: Dict
    seo_keywords: List[str]


class ContentAnalysisAgent:
    """AI-powered content analysis and optimization agent"""

    def __init__(self):
        self.viral_triggers = [
            "shocking",
            "unbelievable",
            "hilarious",
            "insane",
            "crazy",
            "you won't believe",
            "can't make this up",
            "mind-blowing",
            "epic",
            "legendary",
            "iconic",
            "viral moment",
            "must see",
        ]

        self.thumbnail_templates = {
            "reaction": "Split screen of shocked faces + viral text overlay",
            "comparison": "Before/after split with dramatic contrast",
            "secret": "Finger over lips + 'secret revealed' text",
            "challenge": "Progress bar + challenge name + prize emoji",
            "local_pride": "Map highlight + local branding + crown",
            "comedy_gold": "Golden glow + comedy quote + laugh emojis",
        }

        self.comedy_niches = [
            "roanoke comedy king",
            "virginia comedy legend",
            "underground comedy star",
            "comedy's best kept secret",
            "local comedy royalty",
            "rising comedy phenom",
        ]

        self.engagement_strategies = [
            "question_prompt",
            "challenge_comparison",
            "secret_reveal",
            "behind_scenes",
            "exclusive_content",
            "myth_busting",
        ]

    def analyze_content_opportunities(
        self, transcript: str, guest_name: str, video_duration: str
    ) -> VideoMetadata:
        """Analyze content and generate complete metadata package"""

        # Extract key themes and moments
        themes = self._extract_themes(transcript)
        viral_moments = self._identify_viral_moments(transcript)
        seo_keywords = self._generate_seo_keywords(guest_name, themes)

        # Generate thumbnail concepts
        thumbnail_specs = self._generate_thumbnail_concepts(viral_moments, guest_name)

        # Generate content cards
        content_cards = self._generate_content_cards(viral_moments, themes, guest_name)

        # Optimize title and description
        title = self._generate_optimized_title(viral_moments, guest_name, seo_keywords)
        description = self._generate_optimized_description(
            viral_moments, guest_name, themes
        )
        tags = self._generate_optimized_tags(seo_keywords, themes, guest_name)

        # Upload schedule optimization
        upload_schedule = self._generate_upload_schedule(themes, viral_moments)

        return VideoMetadata(
            title=title,
            description=description,
            tags=tags,
            category="Entertainment",
            thumbnail_spec=thumbnail_specs[0],  # Best performing concept
            content_cards=content_cards,
            upload_schedule=upload_schedule,
            seo_keywords=seo_keywords,
        )

    def _extract_themes(self, transcript: str) -> List[str]:
        """Extract main themes from transcript"""
        themes = []
        text_lower = transcript.lower()

        # Theme detection keywords
        theme_keywords = {
            "comedy_career": [
                "comedy",
                "career",
                "stage",
                "perform",
                "stand up",
                "open mic",
            ],
            "personal_stories": [
                "story",
                "childhood",
                "grew up",
                "remember",
                "happened",
            ],
            "local_scene": ["roanoke", "virginia", "local", "venue", "comedy club"],
            "challenges": ["challenge", "dare", "competition", "contest", "tried"],
            "food_reactions": ["eating", "spicy", "pickle", "bean boozled", "reaction"],
            "behind_scenes": ["behind", "backstage", "before", "after", "preparation"],
            "industry_insights": [
                "industry",
                "business",
                "money",
                "booking",
                "agents",
                "gigs",
            ],
        }

        for theme, keywords in theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme)

        return themes if themes else ["comedy_conversations"]

    def _identify_viral_moments(self, transcript: str) -> List[Dict]:
        """Identify potentially viral moments in transcript"""
        viral_moments = []

        # Pattern detection for viral content
        viral_patterns = [
            {
                "type": "shocking_confession",
                "indicators": [
                    "i admit",
                    "confess",
                    "secret",
                    "never told anyone",
                    "reveal",
                ],
                "engagement_potential": 9.0,
            },
            {
                "type": "hilarious_reaction",
                "indicators": [
                    "can't stop laughing",
                    "crying",
                    "dying",
                    "funniest thing",
                ],
                "engagement_potential": 8.5,
            },
            {
                "type": "challenge_gone_wrong",
                "indicators": [
                    "too spicy",
                    "can't handle",
                    "give up",
                    "wrong",
                    "mistake",
                ],
                "engagement_potential": 9.2,
            },
            {
                "type": "local_drama",
                "indicators": [
                    "roanoke",
                    "local comedy scene",
                    "venue",
                    "drama",
                    "story",
                ],
                "engagement_potential": 7.5,
            },
            {
                "type": "industry_secret",
                "indicators": [
                    "industry",
                    "behind the scenes",
                    "what they don't tell you",
                ],
                "engagement_potential": 8.0,
            },
        ]

        text_lower = transcript.lower()
        for pattern in viral_patterns:
            if any(indicator in text_lower for indicator in pattern["indicators"]):
                # Extract relevant text snippet (simplified)
                viral_moments.append(
                    {
                        "type": pattern["type"],
                        "engagement_score": pattern["engagement_potential"],
                        "description": self._generate_moment_description(
                            pattern["type"]
                        ),
                    }
                )

        return sorted(viral_moments, key=lambda x: x["engagement_score"], reverse=True)

    def _generate_moment_description(self, moment_type: str) -> str:
        """Generate compelling description for viral moment"""
        descriptions = {
            "shocking_confession": "Comedian drops a confession that changes everything",
            "hilarious_reaction": "Reaction so funny it breaks the internet",
            "challenge_gone_wrong": "Watch everything go horribly wrong in real-time",
            "local_drama": "The local comedy story everyone's talking about",
            "industry_secret": "What comedians don't want you to know about the business",
        }
        return descriptions.get(moment_type, "Must-see comedy moment")

    def _generate_thumbnail_concepts(
        self, viral_moments: List[Dict], guest_name: str
    ) -> List[ThumbnailSpec]:
        """Generate multiple thumbnail concepts"""
        concepts = []

        if not viral_moments:
            # Default concepts
            concepts.append(
                ThumbnailSpec(
                    concept="Guest Spotlight",
                    colors=["#FF6B35", "#FFFFFF", "#000000"],  # Orange, White, Black
                    text_overlay=f"{guest_name}\\nJAREDSNOTFUNNY",
                    emotion="professional_funny",
                    viral_elements=["microphone", "comedy club logo"],
                )
            )
            return concepts

        top_moment = viral_moments[0]  # Highest engagement potential

        if top_moment["type"] == "shocking_confession":
            concepts.append(
                ThumbnailSpec(
                    concept="Secret Revealed",
                    colors=["#8B0000", "#FFD700", "#FFFFFF"],  # Dark Red, Gold, White
                    text_overlay="SECRET REVEALED\\n🤫 SHOCKING CONFESSION",
                    emotion="shocking_intense",
                    viral_elements=[
                        "shock marks",
                        "question marks",
                        "explosion graphics",
                    ],
                )
            )

        elif top_moment["type"] == "hilarious_reaction":
            concepts.append(
                ThumbnailSpec(
                    concept="Laugh Attack",
                    colors=["#32CD32", "#FFFF00", "#FF1493"],  # Green, Yellow, Dark Red
                    text_overlay="CAN'T BREATHE\\n😂 FUNNIEST REACTION",
                    emotion="hilarious_chaos",
                    viral_elements=["tear marks", "laugh emojis", "sound waves"],
                )
            )

        elif top_moment["type"] == "challenge_gone_wrong":
            concepts.append(
                ThumbnailSpec(
                    concept="Epic Fail",
                    colors=[
                        "#DC143C",
                        "#FF4500",
                        "#FFFFFF",
                    ],  # Crimson, Orange Red, White
                    text_overlay="CHALLENGE FAILED\\n😨 EVERYTHING WENT WRONG",
                    emotion="dramatic_failure",
                    viral_elements=["explosion", "warning signs", "chaos graphics"],
                )
            )

        elif top_moment["type"] == "local_drama":
            concepts.append(
                ThumbnailSpec(
                    concept="Local King",
                    colors=[
                        "#4B0082",
                        "#FFD700",
                        "#8B4513",
                    ],  # Indigo, Gold, Saddle Brown
                    text_overlay="ROANOKE'S COMEDY KING\\n👑 THE STORY",
                    emotion="local_pride",
                    viral_elements=["crown", "map pin", "local landmark"],
                )
            )

        return concepts

    def _generate_content_cards(
        self, viral_moments: List[Dict], themes: List[str], guest_name: str
    ) -> List[ContentCard]:
        """Generate content cards for social media promotion"""
        cards = []

        # Card 1: Main hook card
        if viral_moments:
            top_moment = viral_moments[0]
            cards.append(
                ContentCard(
                    headline=f"🔥 {guest_name} drops the {random.choice(['BOMBSHELL', 'TEA', 'TRUTH'])}",
                    subheadline=top_moment["description"],
                    key_points=[
                        "The moment that broke comedy TikTok",
                        "What comedians say OFF camera",
                        "Behind the scenes footage included",
                    ],
                    call_to_action="Watch the viral moment everyone's talking about",
                    hashtags=[
                        "#jaredsnotfunny",
                        "#viral",
                        "#comedy",
                        "#podcastclips",
                        "#roanoke",
                    ],
                    engagement_prompt="What part shocked you the most? 🤯",
                )
            )

        # Card 2: Niche authority card
        niche_focus = random.choice(self.comedy_niches)
        cards.append(
            ContentCard(
                headline=f"🗺️ Why {guest_name} is {niche_focus}",
                subheadline="The comedy world's best kept secret",
                key_points=[
                    "Local comedy scene authority",
                    "Behind the scenes access",
                    "Stories no one else has",
                    "Authentic comedy conversations",
                ],
                call_to_action="Join the comedy revolution taking over Virginia",
                hashtags=[
                    "#roanokecomedy",
                    "#virginiastandup",
                    "#localcomedy",
                    "#comedy",
                    "#podcast",
                ],
                engagement_prompt="Who's the most underrated comedian in your area? 🎭",
            )
        )

        # Card 3: Value proposition card
        cards.append(
            ContentCard(
                headline="🎭 COMEDY THAT'S ACTUALLY FUNNY",
                subheadline="No scripts, no filters, just real conversations",
                key_points=[
                    "Raw, unfiltered comedy moments",
                    "Local comedians you should know",
                    "Weekly dose of authentic humor",
                    "Building Roanoke's comedy scene",
                ],
                call_to_action="Subscribe for your weekly comedy fix",
                hashtags=[
                    "#authenticcomedy",
                    "#realconversations",
                    "#standup",
                    "#roanoke",
                    "#virginia",
                ],
                engagement_prompt="What do you want to hear next episode? 🎤",
            )
        )

        return cards

    def _generate_optimized_title(
        self, viral_moments: List[Dict], guest_name: str, keywords: List[str]
    ) -> str:
        """Generate SEO and engagement-optimized title"""
        if not viral_moments:
            return f"JAREDSNOTFUNNY feat {guest_name} - Comedy Conversations"

        top_moment = viral_moments[0]
        moment_type = top_moment["type"]

        title_patterns = {
            "shocking_confession": "{guest}'s SHOCKING Comedy Confession 🤫",
            "hilarious_reaction": "{guest} Can't Stop Laughing 😂",
            "challenge_gone_wrong": "When {guest} Tried [Challenge]... 😨",
            "local_drama": "The {guest} Story That Broke Roanoke 🗺️",
            "industry_secret": "What Comedians Don't Want You To Know 🔮",
        }

        base_title = title_patterns.get(moment_type, f"{guest} Hilarious Moment 🔥")

        # Add viral keywords
        viral_trigger = random.choice(self.viral_triggers)
        if random.random() > 0.5:  # 50% chance to add viral trigger
            base_title = f"{viral_trigger.upper()}: {base_title}"

        return base_title.format(
            guest=guest_name.split()[0]
        )  # Use first name for brevity

    def _generate_optimized_description(
        self, viral_moments: List[Dict], guest_name: str, themes: List[str]
    ) -> str:
        """Generate optimized description for SEO and engagement"""
        lines = []

        # Hook line
        if viral_moments:
            top_moment = viral_moments[0]
            lines.append(
                f"🔥 {top_moment['description']} in this hilarious JAREDSNOTFUNNY episode!"
            )

        # Context line
        lines.append(
            f"🎭 {guest_name} joins Jared for raw, authentic comedy conversations about life, comedy, and everything in between."
        )

        # Key moments
        if len(viral_moments) > 1:
            lines.append("\\n📍 KEY MOMENTS:")
            for i, moment in enumerate(viral_moments[:3], 1):
                lines.append(f"   {i}. {moment['description']}")

        # Value proposition
        lines.append("\\n✨ WHY YOU'LL LOVE THIS:")
        lines.append("• Raw, unfiltered comedy conversations")
        lines.append("• Behind the scenes access")
        lines.append("• Local comedy scene insights")
        lines.append("• No scripts, no filters, just real talk")

        # Call to action
        lines.append("\\n🎯 SUBSCRIBE for weekly comedy content!")
        lines.append("🎪 SUPPORT LOCAL COMEDY")
        lines.append("📱 Follow us on TikTok & Instagram: @jaredsnotfunny")
        lines.append("🌐 Website: https://www.jaredsnotfunny.com")

        # Hashtags
        hashtags = ["#jaredsnotfunny", "#comedy", "#podcast", "#standup", "#roanoke"]
        if themes:
            theme_tags = [f"#{theme.replace('_', '')}" for theme in themes[:2]]
            hashtags.extend(theme_tags)

        lines.append(f"\\n🏷️  {' '.join(hashtags[:10])}")

        return "\\n".join(lines)

    def _generate_optimized_tags(
        self, seo_keywords: List[str], themes: List[str], guest_name: str
    ) -> List[str]:
        """Generate comprehensive tag list"""
        tags = []

        # Core tags
        core_tags = [
            "jaredsnotfunny",
            "comedy podcast",
            "stand up comedy",
            "funny conversations",
            "roanoke comedy",
        ]
        tags.extend(core_tags)

        # Guest-specific tags
        if guest_name:
            tags.append(guest_name.lower())
            tags.append(f"{guest_name.lower()} comedy")

        # Theme-based tags
        for theme in themes:
            if theme == "comedy_career":
                tags.extend(
                    [
                        "comedy career",
                        "stand up advice",
                        "comedy business",
                        "comedy industry",
                    ]
                )
            elif theme == "local_scene":
                tags.extend(
                    [
                        "roanoke virginia",
                        "local comedy",
                        "virginia comedy",
                        "comedy club",
                    ]
                )
            elif theme == "challenges":
                tags.extend(
                    [
                        "comedy challenge",
                        "funny challenge",
                        "comedy dare",
                        "challenge reaction",
                    ]
                )

        # SEO keywords
        tags.extend(seo_keywords)

        # Viral/trending tags
        viral_tags = [
            "viral",
            "trending",
            "funny moments",
            "comedy gold",
            "must watch",
            "you wont believe",
        ]
        tags.extend(viral_tags[:5])  # Limit to top 5

        # Remove duplicates and limit to YouTube's 30-tag max
        unique_tags = list(
            dict.fromkeys(tags)
        )  # Preserve order while removing duplicates
        return unique_tags[:30]

    def _generate_seo_keywords(self, guest_name: str, themes: List[str]) -> List[str]:
        """Generate SEO-optimized keywords"""
        keywords = []

        # Primary keywords
        keywords.extend(
            ["jaredsnotfunny podcast", "comedy podcast", "stand up interviews"]
        )

        # Guest keywords
        if guest_name:
            keywords.extend(
                [
                    f"{guest_name} comedy",
                    f"{guest_name} interview",
                    f"{guest_name} podcast",
                ]
            )

        # Theme-based keywords
        theme_keywords = {
            "comedy_career": [
                "comedian career",
                "how to start comedy",
                "comedy business advice",
            ],
            "local_scene": [
                "roanoke comedy scene",
                "virginia stand up",
                "local comedy venues",
            ],
            "challenges": ["comedy challenges", "funny challenges", "comedy reactions"],
            "food_reactions": [
                "food challenge comedy",
                "spicy food reaction",
                "eating comedy",
            ],
        }

        for theme in themes:
            if theme in theme_keywords:
                keywords.extend(theme_keywords[theme])

        # Long-tail keywords
        long_tail = [
            "funny podcast interviews",
            "local comedian interviews",
            "roanoke virginia comedy",
            "stand up comedy conversations",
            "comedy podcast behind the scenes",
            "comedian life stories",
        ]
        keywords.extend(long_tail)

        return keywords[:20]  # Top 20 keywords

    def _generate_upload_schedule(
        self, themes: List[str], viral_moments: List[Dict]
    ) -> Dict:
        """Generate optimal upload schedule"""
        return {
            "primary_upload": {
                "day": "Thursday",
                "time": "7:00 PM EST",
                "reasoning": "Thursday has highest comedy engagement, evening prime time",
            },
            "short_form_posts": {
                "frequency": "Daily",
                "optimal_times": ["12:00 PM", "7:00 PM", "9:00 PM"],
                "platforms": ["TikTok", "YouTube Shorts", "Instagram Reels"],
            },
            "promotional_posts": {
                "frequency": "3x/week",
                "content_types": [
                    "behind scenes",
                    "guest teasers",
                    "episode highlights",
                ],
                "platforms": ["Instagram", "Facebook", "Twitter"],
            },
            "engagement_posts": {
                "frequency": "Daily",
                "content_types": ["polls", "questions", "fan interactions"],
                "platforms": ["Instagram Stories", "Twitter", "TikTok comments"],
            },
        }


def demonstrate_content_analysis():
    """Demonstrate the content analysis and enhancement system"""
    print("🔍 CONTENT ANALYSIS & ENHANCEMENT AGENT")
    print("=" * 60)

    agent = ContentAnalysisAgent()

    # Example content
    sample_transcript = """
    Jared: Welcome to JAREDSNOTFUNNY! Today we have Arthur Stump, one of the funniest comedians in Roanoke.
    Arthur: Thanks Jared! I've got to confess something, I've never told anyone this story about my first time on stage...
    Jared: Oh really? Tell us what happened!
    Arthur: So I get on stage at the local comedy club, and I'm so nervous I forget my entire set...
    [Arthur tells hilarious story about bombing on stage]
    Arthur: And then the manager comes up and says 'Arthur, that was the worst thing I've ever seen'
    [Everyone laughs uncontrollably]
    """

    guest_name = "Arthur Stump"
    duration = "45:30"

    print(f"📝 Analyzing Content: {guest_name} Episode")
    print(f"📊 Transcript Length: {len(sample_transcript)} characters")

    # Analyze content
    metadata = agent.analyze_content_opportunities(
        sample_transcript, guest_name, duration
    )

    print(f"\\n🎯 OPTIMIZED TITLE:")
    print(f"   {metadata.title}")
    print(
        f"   Engagement Score: {agent._calculate_engagement_score(metadata.title, sample_transcript):.1f}/10"
    )

    print(f"\\n🎨 THUMBNAIL CONCEPT:")
    thumb = metadata.thumbnail_spec
    print(f"   Concept: {thumb.concept}")
    print(f"   Colors: {', '.join(thumb.colors)}")
    print(f"   Text: {thumb.text_overlay}")
    print(f"   Emotion: {thumb.emotion}")

    print(f"\\n📱 CONTENT CARDS:")
    for i, card in enumerate(metadata.content_cards, 1):
        print(f"\\n   Card {i}: {card.headline}")
        print(f"      📝 {card.subheadline}")
        print(f"      🎯 CTA: {card.call_to_action}")
        print(f"      📊 Hashtags: {', '.join(card.hashtags[:5])}")

    print(f"\\n🏷️  TOP TAGS (first 10):")
    for tag in metadata.tags[:10]:
        print(f"   • {tag}")

    print(f"\\n📅 UPLOAD SCHEDULE:")
    schedule = metadata.upload_schedule
    print(
        f"   🗓️ Primary Upload: {schedule['primary_upload']['day']} at {schedule['primary_upload']['time']}"
    )
    print(
        f"   📱 Short-Form: {schedule['short_form_posts']['frequency']} at {', '.join(schedule['short_form_posts']['optimal_times'])}"
    )

    # Save complete metadata
    metadata_dict = {
        "title": metadata.title,
        "description": metadata.description,
        "tags": metadata.tags,
        "category": metadata.category,
        "thumbnail_concept": {
            "concept": metadata.thumbnail_spec.concept,
            "colors": metadata.thumbnail_spec.colors,
            "text_overlay": metadata.thumbnail_spec.text_overlay,
            "emotion": metadata.thumbnail_spec.emotion,
            "viral_elements": metadata.thumbnail_spec.viral_elements,
        },
        "content_cards": [
            {
                "headline": card.headline,
                "subheadline": card.subheadline,
                "key_points": card.key_points,
                "call_to_action": card.call_to_action,
                "hashtags": card.hashtags,
                "engagement_prompt": card.engagement_prompt,
            }
            for card in metadata.content_cards
        ],
        "upload_schedule": metadata.upload_schedule,
        "seo_keywords": metadata.seo_keywords,
        "generated_at": datetime.now().isoformat(),
    }

    with open("content_analysis_metadata.json", "w") as f:
        json.dump(metadata_dict, f, indent=2)

    print(f"\\n💾 Complete metadata saved to: content_analysis_metadata.json")
    print("🎉 Ready to optimize and upload content!")


if __name__ == "__main__":
    demonstrate_content_analysis()
