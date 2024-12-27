import requests
from bs4 import BeautifulSoup
import time
import json
from pathlib import Path
import re
from typing import List, Dict
import logging

class F1Scraper:
    def __init__(self, base_url: str = "https://pitwall.app"):
        self.base_url = base_url
        self.session = requests.Session()
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('f1_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_season_races(self, year: int) -> List[Dict]:
        """Get all race URLs for a given season."""
        try:
            url = f"{self.base_url}/races/archive/{year}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            race_links = soup.find_all('a', href=re.compile(f'/races/{year}-.*-grand-prix'))
            
            races = []
            for link in race_links:
                race_url = f"{self.base_url}{link['href']}"
                race_name = link.text.strip()
                races.append({
                    'name': race_name,
                    'url': race_url
                })
            
            self.logger.info(f"Found {len(races)} races for season {year}")
            return races
            
        except Exception as e:
            self.logger.error(f"Error getting season races for {year}: {str(e)}")
            return []

    def get_session_types(self, soup: BeautifulSoup) -> List[str]:
        """Extract all session types from the dropdown menu."""
        session_types = []
        try:
            # Find the select menu
            select_menu = soup.find('div', class_='select-menu')
            if select_menu:
                # Get all options from the dropdown
                options = select_menu.find_all('span', class_='title')
                session_types = [option.text.strip() for option in options]
            
            return session_types
        except Exception as e:
            self.logger.error(f"Error getting session types: {str(e)}")
            return []

    def get_race_data(self, race_url: str) -> Dict:
        """Scrape data for all sessions of a specific race."""
        try:
            response = self.session.get(race_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            session_types = self.get_session_types(soup)
            
            if not session_types:
                self.logger.warning("No session types found in dropdown menu")
                # Still save the main page data
                session_types = ['Race']
            
            sessions_data = {}
            
            for session_type in session_types:
                # If there's a session selector in the URL, use it
                session_param = f"?session={session_type.lower().replace(' ', '_')}"
                session_url = f"{race_url}{session_param}"
                
                session_response = self.session.get(session_url)
                if session_response.status_code == 200:
                    sessions_data[session_type] = session_response.text
                    self.logger.info(f"Retrieved data for {session_type}")
                else:
                    self.logger.warning(f"Failed to get data for {session_type}")
                
                # Be nice to the server
                time.sleep(1)
            
            return sessions_data
            
        except Exception as e:
            self.logger.error(f"Error scraping race data from {race_url}: {str(e)}")
            return {}

    def save_race_data(self, year: int, race_name: str, data: Dict):
        """Save scraped data to files."""
        try:
            # Create directory structure
            base_dir = Path(f"f1_data/{year}/{race_name}")
            base_dir.mkdir(parents=True, exist_ok=True)
            
            # Save each session type
            for session_type, html_content in data.items():
                # Clean filename: remove special characters and spaces
                clean_name = re.sub(r'[^\w\s-]', '', session_type)
                clean_name = clean_name.replace(' ', '_').lower()
                file_path = base_dir / f"{clean_name}.html"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                    
                self.logger.info(f"Saved {session_type} data for {race_name} ({year})")
            
        except Exception as e:
            self.logger.error(f"Error saving data for {race_name} ({year}): {str(e)}")

    def test_single_race(self, race_url: str) -> bool:
        """Test scraping for a single race."""
        try:
            self.logger.info(f"Testing scraping for race: {race_url}")
            
            # First, get the page and check for session types
            response = self.session.get(race_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            session_types = self.get_session_types(soup)
            
            self.logger.info(f"Found session types: {', '.join(session_types)}")
            
            # Get data for all sessions
            race_data = self.get_race_data(race_url)
            
            if not race_data:
                self.logger.error("No data retrieved for test race")
                return False
                
            session_count = len(race_data)
            self.logger.info(f"Successfully retrieved {session_count} sessions")
            
            # Print sample of data retrieved
            for session_type in race_data.keys():
                content_length = len(race_data[session_type])
                self.logger.info(f"Session {session_type}: {content_length} bytes")
                
            return True
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            return False

    def scrape_season(self, year: int):
        """Scrape all races for a given season."""
        races = self.get_season_races(year)
        
        if not races:
            self.logger.error(f"No races found for {year}")
            return
        
        for race in races:
            self.logger.info(f"Scraping {race['name']}")
            race_data = self.get_race_data(race['url'])
            
            if race_data:
                self.save_race_data(year, race['name'], race_data)
            
            # Be nice to the server
            time.sleep(2)

def main():
    scraper = F1Scraper()
    
    # Test with a single race first
    test_url = "https://pitwall.app/races/2023-bahrain-grand-prix"
    if scraper.test_single_race(test_url):
        print("Test successful! Proceeding with full scrape...")
        
        # Scrape entire season
        seasons = list(range(2024, 2025))
        for year in seasons:
            scraper.scrape_season(year)
    else:
        print("Test failed. Please check the logs and try again.")

if __name__ == "__main__":
    main()