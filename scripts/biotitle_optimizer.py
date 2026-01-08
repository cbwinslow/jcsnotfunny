#!/usr/bin/env python3
"""
Bio & Title Optimization Agent
Creates engaging bios and viral-optimized titles for JAREDSNOTFUNNY content
"""

import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ContentVariant:
    """Represents a content variant with engagement metrics"""

    title: str
    bio_text: str
    hooks: List[str]
    cta: str
    engagement_score: float
    seo_score: float
    viral_potential: str  # Low, Medium, High, Explosive


class BioTitleOptimizer:
    """Advanced bio and title optimization for comedy podcast content"""

    def __init__(self):
        self.comedy_keywords = [
            "hilarious",
            "insane",
            "you won't believe",
            "crazy",
            "shocking",
            "brutally honest",
            "roasting",
            "comedy gold",
            "viral moment",
            "must watch",
            "can't make this up",
            "legendary",
            "iconic",
        ]

        self.podcast_formats = [
            "JAREDSNOTFUNNY",
            "Jared's Not Funny",
            "Comedy Podcast",
            "Stand-up Conversations",
            "Roanoke Comedy",
        ]

        self.engagement_triggers = [
            "questions",
            "challenges",
            "secrets",
            "reveals",
            "confessions",
            "first time",
            "never before",
            "exclusive",
            "behind the scenes",
        ]

        self.niche_angles = [
            "local comedy king",
            "roanoke's finest",
            "virginia comedy legend",
            "underground comedy",
            "comedy's best kept secret",
            "rising comedy star",
        ]

    def generate_engaging_bio(
        self, guest_name: str, episode_theme: str, platform: str = "general"
    ) -> List[ContentVariant]:
        """Generate multiple engaging bio variants"""

        base_info = f"Comedy podcast featuring conversations with {guest_name}"

        variants = []

        # Variant 1: Authority Angle
        variants.append(
            ContentVariant(
                title="Roanoke's Hottest Comedy Podcast",
                bio_text=f"🎭 Roanoke's #1 comedy podcast where {guest_name} reveals what REALLY happens behind the mic 🎤\\n\\n🔥 Viral moments | 🤫 Comedy secrets | 🎪 Local legend\\n\\n📺 New episodes weekly - subscribe!\\n\\n#comedy #podcast #roanoke #viral",
                hooks=[
                    "What comedians say OFF camera",
                    "The comedy world's best kept secret",
                    "Behind the scenes of viral moments",
                ],
                cta="Follow for comedy that's actually funny",
                engagement_score=8.5,
                seo_score=9.0,
                viral_potential="High",
            )
        )

        # Variant 2: Viral Moment Angle
        variants.append(
            ContentVariant(
                title="You Won't Believe What Comedians Say When Mic Is Off",
                bio_text=f"🤯 {guest_name} drops the comedy BOMBS in this episode 💣\\n\\n✨ Moment so viral TikTok couldn't handle it\\n🎪 Roanoke comedy royalty\\n\\n📻 Full episode - link in bio\\n\\n#jaredsnotfunny #viral #comedy #podcastclips",
                hooks=[
                    "The moment that broke comedy TikTok",
                    "Comedians' secret weapon revealed",
                    "Why comedy clubs are shaking",
                ],
                cta="Watch the viral moment everyone's talking about",
                engagement_score=9.2,
                seo_score=8.5,
                viral_potential="Explosive",
            )
        )

        # Variant 3: Local Hero Angle
        variants.append(
            ContentVariant(
                title="Putting Roanoke Comedy on the MAP",
                bio_text=f"🗺️ Making Roanoke the comedy CAPITAL of Virginia 🎭\\n\\n{guest_name} spills the tea on local comedy scene 🍵\\n\\n🔥 Stories so good they should be illegal\\n\\n📺 Your weekly dose of Virginia's finest\\n\\n#roanoke #virginiacomedy #localcomedy",
                hooks=[
                    "Why comedians are moving to Roanoke",
                    "Virginia's comedy secret weapon",
                    "The comedy renaissance happening now",
                ],
                cta="Join the comedy revolution taking over Virginia",
                engagement_score=7.8,
                seo_score=9.5,
                viral_potential="High",
            )
        )

        # Platform-specific optimizations
        if platform == "tiktok":
            for variant in variants:
                variant.bio_text = self._optimize_for_tiktok(variant.bio_text)
                variant.cta = "Follow for daily comedy bombs 💣"

        elif platform == "instagram":
            for variant in variants:
                variant.bio_text = self._optimize_for_instagram(variant.bio_text)
                variant.cta = "Link in bio for full episodes 🎭"

        return sorted(variants, key=lambda x: x.engagement_score, reverse=True)

    def generate_viral_titles(
        self, video_content: str, guest_name: str, duration: str
    ) -> List[ContentVariant]:
        """Generate viral-optimized title variants"""

        viral_patterns = [
            # Pattern 1: Shock/Disbelief
            "{trigger} Comedian Said This On Camera 🤯",
            "I Can't Believe {guest_name} Said This 💣",
            "This {viral_element} Moment Broke Comedy 😱",
            # Pattern 2: Secret/Reveal
            "{guest_name}'s Comedy Secret REVEALED 🤫",
            "What Comedians Don't Want You To Know 🔮",
            "Behind the Scenes of Viral Comedy Moment 🎪",
            # Pattern 3: Local Pride
            "Roanoke's {adjective} Comedian Does It Again 🏆",
            "Why {guest_name} is Virginia's Comedy Royalty 👑",
            "The Moment Virginia Comedy Went NATIONAL 🗺️",
            # Pattern 4: Challenge/Reaction
            "{guest_name} vs {challenge} - Who Wins? 🥊",
            "Comedian's {reaction} to {shocking_thing} 🔥",
            "When {guest_name} Tried {dangerous_thing}... 😨",
        ]

        titles = []

        for pattern in viral_patterns:
            title = self._fill_pattern(pattern, video_content, guest_name)

            # Calculate scores
            engagement_score = self._calculate_engagement_score(title, video_content)
            seo_score = self._calculate_seo_score(title, guest_name, video_content)
            viral_potential = self._determine_viral_potential(engagement_score)

            titles.append(
                ContentVariant(
                    title=title,
                    bio_text="",  # Will be filled separately
                    hooks=self._extract_hooks(title),
                    cta=self._generate_cta(title),
                    engagement_score=engagement_score,
                    seo_score=seo_score,
                    viral_potential=viral_potential,
                )
            )

        return sorted(
            titles, key=lambda x: x.engagement_score * x.seo_score, reverse=True
        )

    def _fill_pattern(self, pattern: str, content: str, guest: str) -> str:
        """Fill viral title pattern with content-specific elements"""

        # Extract key elements from content
        triggers = [
            word for word in self.engagement_triggers if word.lower() in content.lower()
        ]
        viral_elements = [
            word for word in self.comedy_keywords if word.lower() in content.lower()
        ]

        replacements = {
            "{trigger}": random.choice(triggers) if triggers else "Shocking",
            "{guest_name}": guest,
            "{viral_element}": random.choice(viral_elements)
            if viral_elements
            else "Comedy Gold",
            "{adjective}": random.choice(
                ["legendary", "unstoppable", "viral", "iconic"]
            ),
            "{reaction}": random.choice(["reaction", "response", "meltdown"]),
            "{challenge}": random.choice(
                ["pickle challenge", "bean boozled", "comedy dare"]
            ),
            "{shocking_thing}": random.choice(
                ["this statistic", "that confession", "these texts"]
            ),
        }

        title = pattern
        for placeholder, replacement in replacements.items():
            title = title.replace(placeholder, replacement)

        return title

    def _calculate_engagement_score(self, title: str, content: str) -> float:
        """Calculate engagement potential score (1-10)"""
        score = 5.0  # Base score

        # Viral keyword bonuses
        viral_words = [
            "viral",
            "shocking",
            "crazy",
            "insane",
            "you won't believe",
            "can't make this up",
        ]
        for word in viral_words:
            if word.lower() in title.lower():
                score += 1.2

        # Engagement trigger bonuses
        trigger_words = [
            "secret",
            "revealed",
            "behind",
            "scenes",
            "exclusive",
            "first time",
        ]
        for word in trigger_words:
            if word.lower() in title.lower():
                score += 1.0

        # Question bonuses (questions drive engagement)
        if "?" in title:
            score += 0.8

        # Emoji bonuses
        if "🤯" in title or "💣" in title or "🔥" in title:
            score += 0.5

        # Length optimization
        if 40 <= len(title) <= 60:  # Sweet spot for titles
            score += 0.3

        return min(score, 10.0)

    def _calculate_seo_score(self, title: str, guest: str, content: str) -> float:
        """Calculate SEO score (1-10)"""
        score = 5.0  # Base score

        # Guest name inclusion
        if guest.lower() in title.lower():
            score += 1.5

        # Comedy keywords
        comedy_keywords = ["comedy", "comedian", "funny", "podcast", "stand up"]
        for keyword in comedy_keywords:
            if keyword.lower() in title.lower():
                score += 0.5

        # Local SEO
        local_keywords = ["roanoke", "virginia", "local"]
        for keyword in local_keywords:
            if keyword.lower() in title.lower():
                score += 0.8

        # JAREDSNOTFUNNY branding
        if "jaredsnotfunny" in title.lower():
            score += 1.0

        return min(score, 10.0)

    def _determine_viral_potential(self, engagement_score: float) -> str:
        """Determine viral potential based on engagement score"""
        if engagement_score >= 8.5:
            return "Explosive"
        elif engagement_score >= 7.0:
            return "High"
        elif engagement_score >= 6.0:
            return "Medium"
        else:
            return "Low"

    def _optimize_for_tiktok(self, bio_text: str) -> str:
        """Optimize bio for TikTok algorithm"""
        tiktok_optimizations = ["💣", "🔥", "🤯", "🎪", "🤫", "⚡"]

        # Add viral emojis
        optimized = bio_text
        for i, emoji in enumerate(tiktok_optimizations[:3]):  # Limit to 3 emojis
            if i < len(bio_text.split("\\n")):
                optimized = optimized.replace("\\n", f" {emoji}\\n", 1)

        # Add TikTok-specific hashtags
        tiktok_hashtags = " #fyp #foryoupage #viral #comedy #funny #tiktok"
        optimized += tiktok_hashtags

        return optimized

    def _optimize_for_instagram(self, bio_text: str) -> str:
        """Optimize bio for Instagram algorithm"""
        # Instagram prefers cleaner, more professional presentation
        instagram_optimized = bio_text.replace("💣", "✨").replace("🤯", "🏆")

        # Add Instagram-specific elements
        ig_elements = "\\n\\n📺 New episodes every Thursday\\n🎭 Link in bio for full episodes\\n📍 Roanoke, VA"
        instagram_optimized += ig_elements

        return instagram_optimized

    def _extract_hooks(self, title: str) -> List[str]:
        """Extract engagement hooks from title"""
        hooks = []

        if "secret" in title.lower():
            hooks.append("Comedy's best kept secret")
        if "behind" in title.lower():
            hooks.append("What really happens off camera")
        if "viral" in title.lower():
            hooks.append("The moment that broke the internet")
        if "?" in title:
            hooks.append("Answer that shocked everyone")

        return hooks if hooks else ["Must-see comedy moment"]

    def _generate_cta(self, title: str) -> str:
        """Generate context-appropriate call to action"""
        if "secret" in title.lower() or "revealed" in title.lower():
            return "Discover the comedy secrets they don't want you to know"
        elif "viral" in title.lower():
            return "Watch the viral moment everyone's talking about"
        elif "?" in title:
            return "Find out the shocking answer"
        else:
            return "You won't want to miss this"


def demonstrate_biotitle_optimization():
    """Demonstrate the bio and title optimization system"""
    print("🎭 JAREDSNOTFUNNY - Bio & Title Optimization System")
    print("=" * 60)

    optimizer = BioTitleOptimizer()

    # Example 1: Generate bios for Toron Rodgers episode
    print("\\n📝 BIO OPTIMIZATION EXAMPLE")
    print("Guest: Toron Rodgers | Theme: Comedy Career Stories")

    bios = optimizer.generate_engaging_bio(
        guest_name="Toron Rodgers",
        episode_theme="comedy career stories and local comedy scene",
        platform="tiktok",
    )

    for i, bio in enumerate(bios, 1):
        print(f"\\n   Variant {i} ({bio.viral_potential} Potential):")
        print(f"      🎭 Title: {bio.title}")
        print(f"      📱 Bio: {bio.bio_text[:100]}...")
        print(f"      🎯 Engagement: {bio.engagement_score}/10")
        print(f"      🔍 SEO Score: {bio.seo_score}/10")
        print(f"      ⚡ Hooks: {', '.join(bio.hooks[:2])}")

    # Example 2: Generate viral titles
    print("\\n\\n🔥 VIRAL TITLE GENERATION EXAMPLE")
    print("Content: Bean Boozled challenge gone wrong, guest can't handle spicy food")

    titles = optimizer.generate_viral_titles(
        video_content="bean boozled challenge comedy reaction spicy food",
        guest_name="Arthur Stump",
        duration="45:30",
    )

    print(f"\\n   Generated {len(titles)} viral title variants:")
    for i, title in enumerate(titles[:5], 1):
        print(f"\\n   {i}. {title.title}")
        print(f"      🎯 Engagement: {title.engagement_score}/10")
        print(f"      🔍 SEO Score: {title.seo_score}/10")
        print(f"      💥 Viral Potential: {title.viral_potential}")
        print(f"      ⚡ Hooks: {', '.join(title.hooks)}")
        print(f"      📣 CTA: {title.cta}")

    # Save examples
    examples = {
        "bio_variants": [
            {
                "title": bio.title,
                "bio": bio.bio_text,
                "engagement_score": bio.engagement_score,
                "seo_score": bio.seo_score,
                "viral_potential": bio.viral_potential,
            }
            for bio in bios
        ],
        "title_variants": [
            {
                "title": title.title,
                "engagement_score": title.engagement_score,
                "seo_score": title.seo_score,
                "viral_potential": title.viral_potential,
                "hooks": title.hooks,
                "cta": title.cta,
            }
            for title in titles[:5]
        ],
    }

    with open("bio_title_examples.json", "w") as f:
        json.dump(examples, f, indent=2)

    print(f"\\n💾 Examples saved to: bio_title_examples.json")
    print("🎉 Ready to create viral content!")


if __name__ == "__main__":
    demonstrate_biotitle_optimization()
