import calendar
import os
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

# Spanish translations
MONTHS_ES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]
DAYS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def generate_calendar_data(year, month):
    cal = calendar.Calendar(firstweekday=0) # Monday first
    weeks = []
    
    month_dates = cal.monthdatescalendar(year, month)
    
    for week in month_dates:
        week_data = []
        for date in week:
            in_month = date.month == month
            week_data.append((date.day, in_month))
        weeks.append(week_data)
        
    return {
        "year": year,
        "month_name": MONTHS_ES[month],
        "day_names": DAYS_ES,
        "weeks": weeks
    }

def create_calendar_png(year, month, output_filename="calendario.png"):
    data = generate_calendar_data(year, month)
    
    # Load Jinja template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/calendar.html')
    
    html_content = template.render(**data)
    
    # Write temporary html
    temp_html = 'temp_calendar.html'
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("Generating high-resolution PNG...")
    # Render with playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # A4 Landscape at 300 DPI: 3508x2480
        page = browser.new_page(viewport={"width": 3508, "height": 2480})
        
        file_path = f"file://{os.path.abspath(temp_html)}"
        page.goto(file_path)
        
        # Wait for fonts to load properly
        page.evaluate('document.fonts.ready')
        
        page.screenshot(path=output_filename, omit_background=True)
        browser.close()
        
    # Clean up temp file
    if os.path.exists(temp_html):
        os.remove(temp_html)

    print(f"Calendar generated successfully: {output_filename}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate a high-res Spanish calendar PNG.")
    parser.add_argument("year", type=int, help="Year (e.g. 2026)")
    parser.add_argument("month", type=int, help="Month (1-12)")
    parser.add_argument("--output", type=str, default=None, help="Output filename")
    
    args = parser.parse_args()
    
    if args.month < 1 or args.month > 12:
        print("Error: Month must be between 1 and 12.")
        exit(1)
        
    output_name = args.output
    if not output_name:
        month_name = MONTHS_ES[args.month].lower()
        output_name = f"calendario_{month_name}_{args.year}.png"
        
    create_calendar_png(args.year, args.month, output_name)
