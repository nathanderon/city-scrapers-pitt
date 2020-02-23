from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from datetime import datetime


class PittWaterSpider(CityScrapersSpider):
    name = "pitt_water"
    agency = "Pittsburgh Water & Sewer Authority"
    timezone = "America/New_York"
    allowed_domains = ["www.pgh2o.com"]
    start_urls = ["https://www.pgh2o.com/news-events/events-meetings?f%5B0%5D=type%3A9"]

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("div.event-details"):
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        t = item.css("span::text").get()
        return t

    def _parse_description(self, item):
        return None

    def _parse_classification(self, item):
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        date = item.css("div.date::text").re("[A-Z][A-z]*.*")
        time = item.css("div.time::text").re("([0-9].*) -")
        date_text = date[0] + ' ' + time[0]
        datetime = datetime.strptime(date_text, '%A, %b %d, %Y %I:%M %p')
        return None

    def _parse_end(self, item):
        date = item.css("div.date::text").re("[A-Z][A-z]*.*")
        time = item.css("div.time::text").re("- ([0-9].*)")
        date_text = date[0] + ' ' + time[0]
        datetime = datetime.strptime(date_text, '%A, %b %d, %Y %I:%M %p')
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
