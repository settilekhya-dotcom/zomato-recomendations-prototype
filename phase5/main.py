import logging
import sys
from typing import Optional
from phase2.main import get_user_preferences
from phase4.recommender import LLMRecommender
from phase5.display import DisplayManager
from phase5.feedback_collector import FeedbackCollector
from phase5.exporter import Exporter

# Configure logging
logging.basicConfig(
    level=logging.ERROR,  # Clean output for Phase 5
    format='%(levelname)s:%(name)s:%(message)s'
)

def run_final_app():
    """
    Final orchestration function for the Zomato AI Recommender.
    Integrates all phases from 1 to 5.
    """
    display = DisplayManager()
    display.print_header()
    
    # 1. Get validated user input (Phase 2)
    user_input = get_user_preferences()
    if not user_input:
        rprint("[bold red]Failed to capture valid user preferences. Goodbye![/bold red]")
        return

    # 2. Get reasoned recommendations (Phase 3 & 4)
    display.print_header() # Re-print header to keep tagline visible after CLI input
    rprint(f"\n[bold cyan]Searching for the best {user_input.cuisine or ''} places in {user_input.city}...[/bold cyan]")
    
    try:
        # We need the structured results for display and export, 
        # and the LLM reasoning for the "Why you'll like it" section.
        recommender = LLMRecommender()
        
        # Get structured response from engine first (Phase 3)
        engine_response = recommender.engine.get_recommendations(user_input, limit=3)
        
        if engine_response.count == 0:
            rprint(f"\n[bold yellow]No restaurants found in {user_input.city} matching your criteria.[/bold yellow]")
            return

        # Get AI reasoning from LLM (Phase 4)
        rprint("[bold magenta]🤖 Consulted Zomato AI for personalized reasoning...[/bold magenta]")
        reasoning = recommender.get_reasoned_recommendations(user_input, limit=3)
        
        # 3. Rich Display (Phase 5)
        display.display_recommendations(engine_response.recommendations, user_input.city)
        
        # Display the AI reasoning block
        rprint("\n" + reasoning + "\n")

        # 4. Action Layer: Feedback & Export
        collector = FeedbackCollector()
        exporter = Exporter()
        
        choice = input("\nWould you like to (E)xport results, (F)eedback, or (Q)uit? [E/F/Q]: ").upper()
        
        if choice == 'E':
            fmt = input("Export format (J)SON or (C)SV? [J/C]: ").upper()
            if fmt == 'J':
                path = exporter.export_to_json(engine_response.recommendations)
                rprint(f"[bold green]Exported to {path}[/bold green]")
            elif fmt == 'C':
                path = exporter.export_to_csv(engine_response.recommendations)
                rprint(f"[bold green]Exported to {path}[/bold green]")
        
        elif choice == 'F':
            rest_idx = int(input(f"Which restaurant (1-{len(engine_response.recommendations)})?: "))
            if 1 <= rest_idx <= len(engine_response.recommendations):
                rest_name = engine_response.recommendations[rest_idx-1].name
                rating = int(input("Rate it (1-5 star): "))
                comment = input("Any comments?: ")
                collector.collect_feedback(rest_name, rating, comment)
                rprint("[bold green]Thank you for your feedback![/bold green]")

    except Exception as e:
        rprint(f"\n[bold red]\u274c An error occurred: {e}[/bold red]")

    display.print_footer()

if __name__ == "__main__":
    from rich import print as rprint
    try:
        run_final_app()
    except KeyboardInterrupt:
        rprint("\n\n[bold yellow]Exiting... Have a great meal![/bold yellow]")
        sys.exit(0)
