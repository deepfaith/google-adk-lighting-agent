import logging
from vertexai.generative_models import FunctionDeclaration, Tool
from dotenv import load_dotenv
from typing import Optional, List

load_dotenv()
logger = logging.getLogger(__name__)

# --- Lighting Product Search Tool ---
async def search_lighting_products(
    product_type: str,
    location: Optional[str] = None,
    max_price: Optional[float] = None,
    min_lumens: Optional[int] = None,
    energy_efficient: Optional[bool] = None,
    color_temperature: Optional[str] = None,
    brand: Optional[str] = None
):
    """
    Searches for lighting products based on criteria.
    """
    logger.info(f"Searching lighting products with: type={product_type}, location={location}, max_price={max_price}")
    
    # This would connect to your product database or API
    # For now, we'll return mock data
    products = [
        {
            "id": "LED-OUT-001",
            "name": "OutdoorBright LED Floodlight",
            "type": "LED Floodlight",
            "price": 189.99,
            "lumens": 12000,
            "location": "outdoor",
            "energy_efficient": True,
            "color_temperature": "5000K",
            "brand": "LightMaster"
        },
        {
            "id": "LED-OUT-002",
            "name": "Industrial LED High Bay",
            "type": "High Bay Light",
            "price": 159.99,
            "lumens": 18000,
            "location": "warehouse",
            "energy_efficient": True,
            "color_temperature": "4000K",
            "brand": "IndustrialLux"
        },
        {
            "id": "LED-IN-001",
            "name": "Office Panel LED Light",
            "type": "LED Panel",
            "price": 89.99,
            "lumens": 4500,
            "location": "indoor office",
            "energy_efficient": True,
            "color_temperature": "3500K",
            "brand": "OfficeLux"
        },
        {
            "id": "LED-IN-002",
            "name": "Kitchen Recessed LED",
            "type": "Recessed Light",
            "price": 45.99,
            "lumens": 900,
            "location": "indoor kitchen",
            "energy_efficient": True,
            "color_temperature": "3000K",
            "brand": "HomeBright"
        },
        {
            "id": "LED-OUT-003",
            "name": "Garden Path Lights",
            "type": "Path Light",
            "price": 29.99,
            "lumens": 300,
            "location": "outdoor garden",
            "energy_efficient": True,
            "color_temperature": "2700K",
            "brand": "GardenGlow"
        },
        {
            "id": "LED-OUT-004",
            "name": "Security Flood Light with Motion Sensor",
            "type": "Security Light",
            "price": 129.99,
            "lumens": 2200,
            "location": "outdoor security",
            "energy_efficient": True,
            "color_temperature": "5000K",
            "brand": "SafeGuard"
        }
    ]
    
    # Filter products based on criteria
    filtered_products = products
    
    # Handle product_type filtering with more flexibility
    if product_type:
        product_type_lower = product_type.lower()
        filtered_products = [p for p in filtered_products if 
                            product_type_lower in p["type"].lower() or 
                            product_type_lower in p["name"].lower()]
    
    if location:
        filtered_products = [p for p in filtered_products if location.lower() in p["location"].lower()]
    if max_price:
        filtered_products = [p for p in filtered_products if p["price"] <= max_price]
    if min_lumens:
        filtered_products = [p for p in filtered_products if p["lumens"] >= min_lumens]
    if energy_efficient is not None:
        filtered_products = [p for p in filtered_products if p["energy_efficient"] == energy_efficient]
    if color_temperature:
        filtered_products = [p for p in filtered_products if color_temperature in p["color_temperature"]]
    if brand:
        filtered_products = [p for p in filtered_products if brand.lower() in p["brand"].lower()]
    
    summary = f"Found {len(filtered_products)} lighting products matching your criteria."
    return {"products": filtered_products, "summary": summary}

# --- Product Details Tool ---
async def get_product_details(product_ids: List[str]):
    """
    Gets detailed information about specific products by their IDs.
    """
    logger.info(f"Getting details for products: {product_ids}")
    
    # This would connect to your product database or API
    # For now, we'll return mock data
    product_details = {
        "LED-OUT-001": {
            "description": "High-performance outdoor LED floodlight perfect for warehouses and industrial spaces. Weather-resistant with 50,000 hour lifespan.",
            "specifications": {
                "dimensions": "12\" x 8\" x 3\"",
                "weight": "5.2 lbs",
                "voltage": "120-277V",
                "mounting": "Wall or pole mount",
                "warranty": "5 years"
            },
            "reviews": {
                "average": 4.7,
                "count": 128
            },
            "installation_notes": "Requires professional installation. IP65 rated for outdoor use."
        },
        "LED-OUT-002": {
            "description": "Energy-efficient high bay LED light designed for warehouses and manufacturing facilities. Provides bright, uniform illumination for large spaces.",
            "specifications": {
                "dimensions": "16\" diameter x 6\" height",
                "weight": "8.3 lbs",
                "voltage": "120-277V",
                "mounting": "Hook or pendant mount",
                "warranty": "7 years"
            },
            "reviews": {
                "average": 4.9,
                "count": 87
            },
            "installation_notes": "Includes mounting hardware. Recommended installation height: 15-30 feet."
        },
        "LED-IN-001": {
            "description": "Slim LED panel light ideal for office ceilings. Provides even, glare-free illumination for productive work environments.",
            "specifications": {
                "dimensions": "24\" x 24\" x 0.5\"",
                "weight": "3.8 lbs",
                "voltage": "120V",
                "mounting": "Recessed or suspended",
                "warranty": "3 years"
            },
            "reviews": {
                "average": 4.5,
                "count": 92
            },
            "installation_notes": "Compatible with standard drop ceilings. Includes mounting hardware."
        },
        "LED-IN-002": {
            "description": "Energy-efficient recessed LED downlight for kitchens and living spaces. Dimmable for customizable lighting levels.",
            "specifications": {
                "dimensions": "6\" diameter x 1.5\" height",
                "weight": "0.9 lbs",
                "voltage": "120V",
                "mounting": "Recessed can",
                "warranty": "5 years"
            },
            "reviews": {
                "average": 4.8,
                "count": 156
            },
            "installation_notes": "Fits standard 6-inch recessed cans. Dimmable with most LED-compatible dimmers."
        },
        "LED-OUT-003": {
            "description": "Solar-powered garden path lights that automatically illuminate at dusk. Weather-resistant design for year-round use.",
            "specifications": {
                "dimensions": "4\" diameter x 15\" height",
                "weight": "0.7 lbs each",
                "power": "Solar with backup battery",
                "runtime": "Up to 8 hours on full charge",
                "warranty": "1 year"
            },
            "reviews": {
                "average": 4.2,
                "count": 213
            },
            "installation_notes": "No wiring required. Simply stake into ground along pathways."
        },
        "LED-OUT-004": {
            "description": "Dual-head security flood light with 180-degree motion detection. Ideal for driveways, yards, and entry points.",
            "specifications": {
                "dimensions": "10\" x 7\" x 6\"",
                "weight": "2.4 lbs",
                "voltage": "120V",
                "detection range": "Up to 40 feet",
                "warranty": "2 years"
            },
            "reviews": {
                "average": 4.6,
                "count": 178
            },
            "installation_notes": "Requires hardwiring to junction box. Adjustable motion sensitivity and light duration."
        }
    }
    
    results = {}
    for product_id in product_ids:
        if product_id in product_details:
            results[product_id] = product_details[product_id]
    
    return {"product_details": results}

# --- Tool Declarations ---
search_products_tool_declaration = FunctionDeclaration(
    name='search_lighting_products',
    description='Searches for lighting products based on criteria like type, location, and price.',
    parameters={
        "type": "object",
        "properties": {
            'product_type': {"type": "string", "description": 'The type of lighting product (e.g., "LED", "floodlight", "high bay").'},
            'location': {"type": "string", "description": 'Where the light will be used (e.g., "indoor", "outdoor", "warehouse").'},
            'max_price': {"type": "number", "description": 'Maximum price in USD.'},
            'min_lumens': {"type": "integer", "description": 'Minimum brightness in lumens.'},
            'energy_efficient': {"type": "boolean", "description": 'Whether the product should be energy efficient.'},
            'color_temperature': {"type": "string", "description": 'Color temperature (e.g., "3000K", "4000K", "5000K").'},
            'brand': {"type": "string", "description": 'Preferred brand name.'}
        },
        "required": ['product_type']
    }
)

product_details_tool_declaration = FunctionDeclaration(
    name='get_product_details',
    description='Gets detailed information about specific products by their IDs.',
    parameters={
        "type": "object",
        "properties": {
            'product_ids': {
                "type": "array",
                "items": {"type": "string"},
                "description": 'List of product IDs to get details for.'
            }
        },
        "required": ['product_ids']
    }
)

# Create the tools with proper function declarations
SEARCH_PRODUCTS_VERTEX_TOOL = Tool(
    function_declarations=[search_products_tool_declaration]
)

PRODUCT_DETAILS_VERTEX_TOOL = Tool(
    function_declarations=[product_details_tool_declaration]
)

# Make sure the function names match exactly what's in the function declarations
AVAILABLE_LIGHTING_TOOLS = {
    "search_lighting_products": search_lighting_products,
    "get_product_details": get_product_details,
}
