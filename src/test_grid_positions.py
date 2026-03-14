"""
Test script to display fetched grid positions from the API
and the respective race information
"""

from api_handler import get_latest_qualifying, qualifying_to_dataframe, BASE_URL
from datetime import datetime
import pandas as pd


def test_grid_positions():
    print("=" * 80)
    print("API REQUEST INFORMATION")
    print("=" * 80)
    
    # Show what request we're making
    api_endpoint = "current/last/qualifying.json"
    full_url = f"{BASE_URL}/{api_endpoint}"
    
    print(f"\nBase URL:      {BASE_URL}")
    print(f"Endpoint:      {api_endpoint}")
    print(f"Full Request:  {full_url}")
    print(f"Method:        GET")
    print(f"Response Type: JSON")
    
    print("\n" + "=" * 80)
    print("FETCHING LATEST QUALIFYING DATA FROM API")
    print("=" * 80)
    
    try:
        # Fetch latest qualifying from API
        latest_qual = get_latest_qualifying()
        
        if not latest_qual:
            print("❌ No qualifying data found")
            return
        
        print(f"\n✓ Successfully fetched data from API")
        print(f"Number of races with qualifying data: {len(latest_qual)}")
        
        # Get the first (and usually only) race
        race = latest_qual[0]
        
        # Display race information
        print("\n" + "=" * 80)
        print("RACE INFORMATION")
        print("=" * 80)
        print(f"Race Name:     {race['raceName']}")
        print(f"Season:        {race['season']}")
        print(f"Round:         {race['round']}")
        print(f"Date:          {race['date']}")
        print(f"Circuit:       {race['Circuit']['circuitName']} ({race['Circuit']['circuitId']})")
        
        location = race['Circuit'].get('Location', {})
        if location:
            loc_str = location.get('locality', '')
            country = location.get('country', '')
            if not loc_str:
                loc_str = location.get('city', location.get('place', ''))
            print(f"Location:      {loc_str}, {country}")
        
        # Convert to DataFrame for better display
        print("\n" + "=" * 80)
        print("GRID POSITIONS (QUALIFYING RESULTS)")
        print("=" * 80)
        
        df = qualifying_to_dataframe(latest_qual)
        
        print(f"\nTotal Drivers: {len(df)}\n")
        
        # Display grid positions
        display_df = df[[
            "grid_position", 
            "driver_name", 
            "constructor_name",
            "driverId",
            "constructorId"
        ]].copy()
        
        display_df.columns = ["Grid Pos", "Driver", "Constructor", "Driver ID", "Constructor ID"]
        display_df = display_df.sort_values("Grid Pos")
        
        # Print with formatting
        print(f"{'Grid':<6} {'Driver':<30} {'Constructor':<20} {'Driver ID':<15} {'Constructor ID':<18}")
        print("-" * 89)
        
        for idx, row in display_df.iterrows():
            print(f"{row['Grid Pos']:<6} {row['Driver']:<30} {row['Constructor']:<20} {row['Driver ID']:<15} {row['Constructor ID']:<18}")
        
        # Summary statistics
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Latest Race Fetched:  {race['raceName']}")
        print(f"Total Drivers:        {len(df)}")
        print(f"Fetch Timestamp:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data Source:          Ergast API (https://api.jolpi.ca/ergast/f1)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_grid_positions()
