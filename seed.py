from models import db, User, BlogPost, Comment
from datetime import date
from werkzeug.security import generate_password_hash


def seed_demo_data():
    if User.query.first():
        return

    # example users
    admin = User(
        email="admin@example.com",
        name="Admin",
        password=generate_password_hash("adminpass", method='pbkdf2:sha256', salt_length=8)
    )
    jane = User(
        email="janeDOE123@gmail.com",
        name="Jane Doe",
        password=generate_password_hash("password123", method='pbkdf2:sha256', salt_length=8)
    )
    john = User(
        email="johnSmth@gmail.com",
        name="John Smith",
        password=generate_password_hash("securepass", method='pbkdf2:sha256', salt_length=8)
    )
    jack = User(
        email="iamjack4@gmail.com",
        name="Jack Lewis",
        password=generate_password_hash("userpass", method='pbkdf2:sha256', salt_length=8)
    )
    lucy = User(
        email="lulu82@gmail.com",
        name="Lucy Pan",
        password=generate_password_hash("custompass", method='pbkdf2:sha256', salt_length=8)
    )


    db.session.add_all([admin, jane, john, jack, lucy])
    db.session.commit()

    # example blog posts
    post1 = BlogPost(
        title="The Lost Art of Letter Writing in a Digital World",
        subtitle="Why putting pen to paper might be the mindful practice you didn't know you needed",
        body="<p>In an age where we fire off dozens of texts and emails daily, the simple "
             "act of writing a letter by hand has become almost revolutionary. "
             "There's something deeply satisfying about the scratch of pen on paper, "
             "the deliberate pace that forces you to choose your words carefully, and "
             "the tangible connection it creates between writer and recipient.</p><p>Unlike digital "
             "messages that disappear into the void of notifications, a handwritten letter "
             "is a physical artifact that can be held, reread, and treasured. It demands "
             "presence from both the writer and the reader, creating a rare moment of undivided "
             "attention in our fractured world. Perhaps it's time to rediscover this forgotten "
             "form of communication, not as a nostalgic novelty, but as a meaningful way to slow "
             "down and truly connect.</p> <p>Letter writing isn’t just a medium—it’s a mood. The time "
             "it takes to sit, write, and send a letter fosters reflection in a way few digital formats "
             "do. There's a vulnerability in handwriting that can't be hidden behind spellcheck or "
             "curated emoji reactions. Each ink smudge and crossed-out word speaks volumes about "
             "presence, intent, and authenticity.</p> <p>Moreover, writing letters can serve as a "
             "therapeutic ritual. The slow rhythm of writing allows thoughts to untangle, making space "
             "for clarity and calm. In a culture obsessed with speed and efficiency, perhaps there's "
             "quiet power in choosing something slower, more intentional, and deeply human.</p>",
        img_url="https://images.unsplash.com/photo-1559235298-bf3e8ed34441?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        author=admin,
        date=date.today().strftime("%B %d, %Y")
    )
    post2 = BlogPost(
        title="The Strange Reality of Living on Mars",
        subtitle="What science fiction gets wrong about humanity's next home",
        body="<p>While billionaires race to put humans on Mars, the reality of actually living "
             "there would be far stranger and more challenging than most people imagine. "
             "Forget the romantic notions of red sunsets and pioneering adventures - "
             "Martian colonists would face psychological isolation that makes Antarctic "
             "research stations look social, radiation exposure that requires living mostly "
             "underground, and a six-month communication delay with Earth that would make "
             "getting tech support truly impossible.</p><p>The human body, evolved for Earth's "
             "gravity and atmosphere, would undergo changes we're only beginning to "
             "understand. Bones would weaken, muscles would atrophy despite exercise, and "
             "the low atmospheric pressure would affect everything from how wounds heal to "
             "how food tastes. Perhaps most unsettling of all, colonists would need to accept "
             "that Mars might be a one-way trip, as the physical and logistical challenges "
             "of return journeys remain largely unsolved.</p> <p>And then there's the question of "
             "community. On Mars, social dynamics would be magnified by scarcity, confinement, and "
             "isolation. Every disagreement could carry life-or-death consequences, and leadership "
             "would require not only technical skill but profound emotional intelligence. Life on Mars "
             "would test not only our engineering prowess, but our ability to coexist in extreme "
             "environments.</p> <p>Even if we conquer the technological hurdles, the philosophical "
             "ones remain. What does it mean to start life on a new planet? What culture do we bring and "
             "what might we leave behind? Mars colonisation, if it happens, won't just be a scientific "
             "leap; it will be a profound reimagining of what it means to be human.</p>",
        img_url="https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2113&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        author=admin,
        date=date.today().strftime("%B %d, %Y")
    )
    post3 = BlogPost(
        title="Why Your Houseplants Keep Dying",
        subtitle="The surprising psychology behind plant parenthood and what it reveals about life",
        body="<p>Before you blame your black thumb for another fallen fiddle leaf fig, "
             "consider this: your plant casualties might say less about your gardening skills "
             "and more about your relationship with responsibility and routine. Most plant "
             "deaths aren't caused by too little water or insufficient sunlight, but by "
             "inconsistent care patterns that mirror our chaotic modern lifestyles.</p><p>"
             "Plants thrive on predictability, something many of us struggle to provide even "
             "for ourselves. They need regular watering schedules, consistent lighting, and "
             "gradual changes rather than dramatic interventions. Sound familiar? Learning to "
             "care for plants successfully often means learning to create sustainable routines "
             "and realistic expectations, skills that translate surprisingly well to other "
             "areas of life.</p> <p>On a deeper level, our relationship with plants often reflects "
             "how we care for ourselves. Neglect a plant, and it wilts; overwater it in a moment of "
             "guilt, and it drowns. The same goes for how we treat our bodies and minds. Too much or "
             "too little can both do harm. Houseplants, in a way, serve as subtle mirrors for our "
             "internal states.</p> <p>This is why plant parenthood can be such a powerful entry point "
             "into mindfulness. When we start noticing what our plants need—light, water, "
             "attention—we might begin to notice our own unmet needs too. Caring for them can be a "
             "quiet daily reminder to slow down, breathe, and tend to the essentials.</p>",
        img_url="https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=2074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        author=admin,
        date=date.today().strftime("%B %d, %Y")
    )
    post4 = BlogPost(
        title="The Unseen Cost of Infinite Scroll",
        subtitle="How modern app design hijacks our attention and what we can do about it",
        body="<p>We’ve all experienced it—opening a social media app for a quick check and "
         "resurfacing an hour later, dazed and wondering where the time went. This isn't "
         "an accident. Infinite scroll, autoplay, and algorithmic feeds are all engineered "
         "to keep you engaged for as long as possible.</p>"
         "<p>While these features can make digital experiences smoother, they also exploit "
         "our brain's reward systems. The lack of natural stopping cues makes it easy to "
         "lose track of time, affecting productivity, sleep, and even self-esteem. Taking "
         "back control means becoming aware of these design choices and setting boundaries. "
         "From screen time limits to using minimalist apps, we can reclaim our attention, "
         "one swipe at a time.</p> <p>What makes infinite scroll particularly insidious "
         "is its subtlety. It’s not just addictive, it feels frictionless. We rarely "
         "notice how we’re being guided, nudged, and nudged again into longer sessions "
         "and deeper rabbit holes. It’s the modern version of the slot machine, except "             "the currency is your attention.</p> <p>But awareness is the first step toward "
         "reclaiming autonomy. Start by noticing the moments when you scroll out of habit "
         "rather than intention. Design your digital life with the same care you’d give "
         "to your physical space. After all, time is non-renewable; every scroll comes "
         "at a cost.</p>",
        img_url="https://images.unsplash.com/photo-1563168206-6920c1377fa6?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        author=admin,
        date=date.today().strftime("%B %d, %Y")
    )
    post5 = BlogPost(
        title="The Unexpected Power of Doing Nothing",
        subtitle="Why intentional idleness might be the secret to your next breakthrough",
        body="<p>In a world obsessed with hustle and optimisation, doing nothing has become a "
         "radical act. But far from being lazy, deliberate idleness has a long history of "
         "fostering creativity, clarity, and emotional resilience. Think of Einstein's daydreaming "
         "or Virginia Woolf’s walks—stillness was their secret weapon.</p>"
         "<p>When we step back from the constant noise, our minds have space to connect ideas, "
         "process emotions, and reset. Neuroscience even backs this up: the brain’s default mode "
         "network activates during rest, helping with introspection and problem-solving. So the next "
         "time you're tempted to fill every minute, remember that doing nothing might be the most productive "
         "thing you do all day.</p> <p>In fact, some of our most profound moments—epiphanies, "
         "emotional breakthroughs, creative sparks—emerge not in the doing, but in the pausing. "
         "The white space in our days is where ideas percolate, insights crystallise, and rest "
         "recalibrates us for what’s next. It's not just that nothingness isn’t wasted time; "
         "it’s essential time.</p> <p>Building space for intentional idleness doesn’t require "
         "a cabin in the woods. It might be a walk without a podcast, a few quiet minutes "
         "before bed, or simply sitting with a cup of tea and letting your mind wander. In "
         "that silence, you might just hear something important: your own thoughts.</p>",
        img_url="https://images.unsplash.com/reserve/YEc7WB6ASDydBTw6GDlF_antalya-beach-lulu.jpg?q=80&w=1301&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        author=admin,
        date=date.today().strftime("%B %d, %Y")
    )
    post6 = BlogPost(
        title="The Forgotten Foods That Once Ruled the World",
        subtitle="A culinary journey through ancient staples that shaped civilisations",
        body="<p>Before quinoa was a superfood and kale trended on Instagram, ancient grains like "
         "amaranth, millet, and teff nourished empires. These once-essential crops fed societies "
         "from the Aztecs to the Ethiopians, offering not just nutrition, but cultural and spiritual "
         "value as well.</p> <p>Many of these ingredients have faded from modern plates, replaced by industrial agriculture’s "
         "narrow focus on wheat, corn, and rice. But now, there's a growing movement to bring them back—"
         "celebrated for their resilience, biodiversity, and deep historical roots. Exploring these ancient "
         "foods isn’t just a culinary adventure; it’s a way to reconnect with the past while building a more "
         "sustainable future.</p> <p>These ancient grains are more than nutritional powerhouses, they’re also "
         "climate-resilient, often thriving in arid or marginal soils where modern monocultures "
         "would fail. As we face increasing environmental instability, reintroducing these "
         "crops could help build food systems that are both robust and regenerative.</p> "
         "<p>Reviving these foods also means restoring lost cultural heritage. Recipes passed "
         "down for generations, once dismissed as relics, are being rediscovered by chefs and "
         "home cooks alike. In every bite of injera made with teff or a porridge of amaranth "
         "lies a story of human ingenuity, survival, and connection to the land.</p>",
        img_url="https://images.unsplash.com/photo-1632756757343-ed6558b97671?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        author=admin,
        date=date.today().strftime("%B %d, %Y")
    )
    db.session.add_all([post1, post2, post3, post4, post5, post6])
    db.session.commit()

    # example comments
    c1 = Comment(text="Totally agree! I've been sending handwritten thank you notes to clients and the response has been incredible. "
                      "In a world of digital noise, analog stands out.", comment_author=jane, parent_post=post1)
    c2 = Comment(text="Beautiful piece. I travel constantly for work and started leaving handwritten notes for my kids when I'm away. "
                      "They keep every single one in a shoebox under the bed.", comment_author=john, parent_post=post1)
    c3 = Comment(text="There's something so intentional about handwritten words", comment_author=jack, parent_post=post1)
    c4 = Comment(text="This post beautifully captures the intimacy of handwritten letters. It’s fascinating how something so simple can feel so radical today. "
                      "Definitely makes me want to slow down and write a note to someone I care about.", comment_author=lucy, parent_post=post1)
    c5 = Comment(text="OMG yes! I realised my plant failures coincided with my most chaotic life periods. Now I use my watering schedule "
                      "as a mindfulness practice and both my plants and I are thriving!", comment_author=jack, parent_post=post3)
    c6 = Comment(text="I never thought of plant care as a reflection of my own routine, but this really hit home. "
                      "A great reminder that consistency matters. Not just for greenery, but for life too.", comment_author=lucy, parent_post=post3)
    c7 = Comment(text="As a botanist, I can confirm this is spot on. The number of patients... I mean plant parents... who bring me 'mystery' "
                      "plant deaths that are just inconsistent care is astounding.", comment_author=jane, parent_post=post3)
    c8 = Comment(text="This explains so much! I thought I was terrible with plants but really I was just terrible with routines. Started simple "
                      "with a snake plant and worked my way up. Game changer.", comment_author=john, parent_post=post3)
    c9 = Comment(text="This was a much-needed dose of realism amid all the Mars hype. I hadn't considered how isolating and physically "
                      "demanding it would truly be. Makes me appreciate Earth a bit more!", comment_author=lucy, parent_post=post2)
    c10 = Comment(text="Finally someone talking about the real challenges! The psychological aspects are hugely underestimated. We can't even "
                      "handle long-term isolation on Earth properly.", comment_author=john, parent_post=post2)
    c11 = Comment(text="The radiation shielding alone would require living in what's essentially a bunker. All those sci-fi movies with people walking "
                      "around on the surface in thin suits are pure fantasy.", comment_author=jack, parent_post=post2)
    c12 = Comment(text="The communication delay point is fascinating - imagine being truly cut off from human civilisation for the first time in history. "
                      "What would that do to our sense of identity as earthlings?", comment_author=jane, parent_post=post2)
    c13 = Comment(text="This hit hard! It's scary how often I lose track of time just scrolling without meaning to. "
                       "These apps are definitely designed to trap you.", comment_author=jack, parent_post=post4)
    c14 = Comment(text="Really appreciate this breakdown of how the design works against us. It’s not just about "
                       "willpower, it’s about awareness.", comment_author=jane, parent_post=post4)
    c15 = Comment(text="I started using grayscale mode on my phone after reading something similar. "
                       "Made a huge difference to my screen time.", comment_author=lucy, parent_post=post4)
    c16 = Comment(text="It’s wild to think that something as simple as a scroll bar is responsible for so much "
                       "of our lost time and attention. Great post.", comment_author=john, parent_post=post4)
    c17 = Comment(text="I love this perspective. We need more encouragement to step back and just exist for a "
                       "moment without guilt.", comment_author=john, parent_post=post5)
    c18 = Comment(text="Doing nothing feels counterintuitive in today’s world, but I’ve had some of my best ideas when I wasn’t "
                       "trying to be productive.", comment_author=jack,parent_post=post5)
    c19 = Comment(text="Really reminds me of how creativity often comes when you're not forcing it. Even science supports this? "
                       "That’s awesome.", comment_author=jane, parent_post=post5)
    c20 = Comment(text="This made me feel a little less guilty about taking slow mornings. Thank you for reframing rest as something "
                       "valuable.", comment_author=lucy, parent_post=post5)
    c21 = Comment(text="So cool to learn about these ancient grains. I’ve tried teff before in injera, but had no "
                       "idea about its history.", comment_author=jane, parent_post=post6)
    c22 = Comment(text="Love how this connects food to culture and sustainability. Definitely going to explore more diverse grains in my cooking.", comment_author=jack, parent_post=post6)
    c23 = Comment(text="The idea that these foods could help with biodiversity and climate resilience is really powerful. Great insight.", comment_author=lucy, parent_post=post6)
    c24 = Comment(text="I never realised how narrow our modern food system had become. This post opened my eyes to the richness we've lost.", comment_author=john, parent_post=post6)

    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12,
                        c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23, c24])
    db.session.commit()