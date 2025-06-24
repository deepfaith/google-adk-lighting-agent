import logging
from vertexai.generative_models import FunctionDeclaration, Tool
from dotenv import load_dotenv
from typing import Optional, List, Dict

load_dotenv()
logger = logging.getLogger(__name__)

# --- Book Outline Generation Tool ---
async def generate_book_outline(
    genre: str,
    title: Optional[str] = None,
    main_character: Optional[str] = None,
    setting: Optional[str] = None,
    theme: Optional[str] = None,
    num_chapters: Optional[int] = 10
):
    """
    Generates a book outline based on provided parameters.
    """
    logger.info(f"Generating book outline for: genre={genre}, title={title}, chapters={num_chapters}")
    
    # Mock data - in a real implementation, this would use the LLM to generate an outline
    if genre.lower() == "mystery":
        outline = [
            {
                "title": "The Mysterious Disappearance",
                "sections": ["Introduction to the detective", "The crime scene", "Initial clues"]
            },
            {
                "title": "Gathering Evidence",
                "sections": ["Interviewing witnesses", "Forensic analysis", "The detective's theory"]
            },
            {
                "title": "The First Suspect",
                "sections": ["Background investigation", "The alibi", "Hidden motives"]
            },
            {
                "title": "A Surprising Twist",
                "sections": ["New evidence emerges", "The timeline inconsistency", "Revised theories"]
            },
            {
                "title": "The Detective's Dilemma",
                "sections": ["Personal conflicts", "Pressure from authorities", "A moral quandary"]
            },
            {
                "title": "Following the Money",
                "sections": ["Financial investigations", "Uncovering corruption", "The hidden connection"]
            },
            {
                "title": "The Second Murder",
                "sections": ["Escalation", "Pattern recognition", "Public panic"]
            },
            {
                "title": "Breaking Point",
                "sections": ["The detective's revelation", "Confronting the truth", "Setting the trap"]
            },
            {
                "title": "The Final Confrontation",
                "sections": ["Face to face with the killer", "The confession", "Justice served"]
            },
            {
                "title": "Aftermath",
                "sections": ["Tying up loose ends", "Character resolutions", "The final twist"]
            }
        ]
    elif genre.lower() == "fantasy":
        outline = [
            {
                "title": "The Ordinary World",
                "sections": ["Introduction to the protagonist", "Life in the village", "Strange omens"]
            },
            {
                "title": "The Call to Adventure",
                "sections": ["The prophecy revealed", "Reluctance and doubt", "Meeting the mentor"]
            },
            {
                "title": "Crossing the Threshold",
                "sections": ["Leaving home", "First challenges", "New companions"]
            },
            {
                "title": "The Magical Forest",
                "sections": ["Supernatural encounters", "Learning magic", "The first test"]
            },
            {
                "title": "The Ancient City",
                "sections": ["Political intrigue", "Hidden allies", "Discovering ancient knowledge"]
            },
            {
                "title": "The Dark Lord's Minions",
                "sections": ["First confrontation", "A narrow escape", "The cost of victory"]
            },
            {
                "title": "The Betrayal",
                "sections": ["Trust broken", "Separated from allies", "Moment of despair"]
            },
            {
                "title": "The Secret Weapon",
                "sections": ["Ancient artifact discovered", "Learning its power", "Preparing for battle"]
            },
            {
                "title": "The Final Battle",
                "sections": ["Confronting the Dark Lord", "Sacrifice and heroism", "Victory at a cost"]
            },
            {
                "title": "Return with the Elixir",
                "sections": ["A changed world", "Healing the land", "The hero's legacy"]
            }
        ]
    else:
        # Generic outline for any other genre
        outline = [
            {"title": f"Chapter {i}", "sections": [f"Section {i}.1", f"Section {i}.2", f"Section {i}.3"]} 
            for i in range(1, num_chapters + 1)
        ]
    
    summary = f"Created a {genre} book outline with {len(outline)} chapters."
    return {"outline": outline, "summary": summary}

# --- Chapter Writing Tool ---
async def write_chapter(
    chapter_number: int,
    chapter_title: str,
    previous_content: Optional[str] = None,
    style: Optional[str] = None,
    word_count: Optional[int] = 1000
):
    """
    Writes a chapter based on the outline and previous content.
    """
    logger.info(f"Writing chapter {chapter_number}: {chapter_title}")
    
    # Mock data - in a real implementation, this would use the LLM to generate chapter content
    if "mysterious" in chapter_title.lower():
        content = """The fog hung low over the city that morning, shrouding the streets in a ghostly veil. Detective Sarah Morgan pulled her coat tighter as she ducked under the police tape. This was the third crime scene this month with the same signature, and the pressure to find the perpetrator was mounting.

"What do we have?" she asked, approaching the forensic technician who was crouched beside the outline of a body.

"Female victim, mid-thirties. Same calling card as the others," he replied, pointing to a small origami swan placed deliberately on the victim's chest. "Time of death estimated between midnight and 2 AM."

Sarah frowned, taking in the scene methodically. The location was different this time – an upscale neighborhood instead of the industrial areas where the previous victims had been found. The killer was evolving, getting bolder. Or maybe sending a message.

Her phone buzzed. It was the captain, no doubt calling for an update she didn't have. Sarah took a deep breath before answering, watching as the morning light struggled to penetrate the thick fog. Something about this case felt different. Personal, somehow. And she couldn't shake the feeling that they were running out of time."""
    elif "adventure" in chapter_title.lower():
        content = """The ancient map trembled in Elian's hands as he stood at the edge of the Whispering Woods. According to local legend, no one who had ventured more than a league into its depths had ever returned. Yet here he was, about to do exactly that.

"You don't have to come with me," he said to Kira, who was checking the straps on her pack for the third time. "The prophecy only mentioned one traveler."

Kira snorted. "Prophecies are notoriously bad at details. Besides, you wouldn't last two days without me."

She wasn't wrong. While Elian had the knowledge of ancient languages and symbols needed to find the Crystal of Azaroth, Kira had the practical skills that would keep them alive in the wilderness.

The sun was beginning its descent toward the horizon. If they were going to make it to the first safe haven before nightfall, they needed to leave now.

"Ready?" Elian asked, tucking the map into his leather satchel.

Kira drew her short sword and tested its edge with her thumb. "Born ready," she replied with a grin that didn't quite reach her eyes.

Together, they took their first steps under the ancient canopy, where the trees grew so tall and thick that they seemed to form a cathedral of wood and leaf. Neither of them noticed the hooded figure watching from the hill behind them, or the raven that took flight at his silent command."""
    else:
        content = f"This is the content for Chapter {chapter_number}: {chapter_title}. This would be a fully written chapter of approximately {word_count} words, continuing the story from previous chapters and developing the plot according to the outline."
    
    return {
        "chapter_content": {
            "title": chapter_title,
            "number": chapter_number,
            "content": content,
            "word_count": len(content.split())
        }
    }

# --- Tool Declarations ---
generate_outline_tool_declaration = FunctionDeclaration(
    name='generate_book_outline',
    description='Generates a book outline based on genre, title, and other parameters.',
    parameters={
        "type": "object",
        "properties": {
            'genre': {"type": "string", "description": 'The genre of the book (e.g., "mystery", "fantasy", "romance").'},
            'title': {"type": "string", "description": 'The title of the book (optional).'},
            'main_character': {"type": "string", "description": 'Description of the main character (optional).'},
            'setting': {"type": "string", "description": 'The setting of the story (optional).'},
            'theme': {"type": "string", "description": 'The main theme or message of the book (optional).'},
            'num_chapters': {"type": "integer", "description": 'Number of chapters to include in the outline.'}
        },
        "required": ['genre']
    }
)

write_chapter_tool_declaration = FunctionDeclaration(
    name='write_chapter',
    description='Writes a chapter based on the outline and previous content.',
    parameters={
        "type": "object",
        "properties": {
            'chapter_number': {"type": "integer", "description": 'The chapter number to write.'},
            'chapter_title': {"type": "string", "description": 'The title of the chapter.'},
            'previous_content': {"type": "string", "description": 'Content from previous chapters for continuity (optional).'},
            'style': {"type": "string", "description": 'Writing style to use (e.g., "descriptive", "dialogue-heavy") (optional).'},
            'word_count': {"type": "integer", "description": 'Approximate word count for the chapter (optional).'}
        },
        "required": ['chapter_number', 'chapter_title']
    }
)

# Create the tools with proper function declarations
GENERATE_OUTLINE_VERTEX_TOOL = Tool(
    function_declarations=[generate_outline_tool_declaration]
)

WRITE_CHAPTER_VERTEX_TOOL = Tool(
    function_declarations=[write_chapter_tool_declaration]
)

# Make sure the function names match exactly what's in the function declarations
AVAILABLE_WRITING_TOOLS = {
    "generate_book_outline": generate_book_outline,
    "write_chapter": write_chapter,
}