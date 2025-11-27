import yaml
import sys
import json

from .validator import SchemaValidator

# URLs for the JSON schemas
JSON_RESUME_SCHEMA_URL = (
    "https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json"
)
RENDER_CV_SCHEMA_URL = (
    "https://raw.githubusercontent.com/sinaatalay/rendercv/main/schema.json"
)


class JSONResumeConverter:
    # RenderCV supported social network enum options
    networks = {
        "github": "GitHub",
        "gitlab": "GitLab",
        "google_scholar": "Google Scholar",
        "instagram": "Instagram",
        "linkedin": "LinkedIn",
        "mastodon": "Mastodon",
        "orcid": "ORCID",
        "research_gate": "ResearchGate",
        "stackoverflow": "StackOverflow",
        "youtube": "YouTube",
    }
    default_network = "github"

    def __init__(self, json_resume):
        self.json_resume = json_resume
        basics = json_resume["basics"]
        
        # Build cv dict with required fields
        cv_dict = {
            "name": basics["name"],
            "email": basics["email"],
            "phone": basics["phone"],
            "sections": {},
        }
        
        # Add optional fields only if they have valid values
        location = self.format_location(basics.get("location"))
        if location:
            cv_dict["location"] = location
            
        if basics.get("url"):
            cv_dict["website"] = basics["url"]
            
        social_networks = self.format_social_networks(basics.get("profiles", []))
        if social_networks:
            cv_dict["social_networks"] = social_networks
        
        self.render_cv = {"cv": cv_dict}

        sections = {}
        
        # Add summary if present
        if basics.get("summary"):
            sections["summary"] = [basics["summary"]]
            
        sections.update({
            "education": self.format_education(json_resume.get("education", [])),
            "experience": self.format_experience(json_resume.get("work", [])),
            "publications": self.format_publications(
                json_resume.get("publications", [])
            ),
            "projects": self.format_projects(json_resume.get("projects", [])),
            "technologies": self.format_technologies(json_resume.get("skills", [])),
            "awards": self.format_awards(json_resume.get("awards", [])),
        })

        # Removing optional sections when empty
        for key, section in sections.items():
            if len(section) > 0:
                self.render_cv["cv"]["sections"][key] = section

    def format_location(self, location):
        if location:
            return f"{location['city']}, {location['countryCode']}"
        return None

    def format_social_networks(self, profiles):
        social_networks = []
        for profile in profiles:
            network_key = profile["network"].lower()
            network = self.networks.get(network_key)
            if not network:
                print(f"Falling back to default network: {self.default_network}")
                network = self.networks.get(self.default_network)

            social_network = {
                "network": network,
                "username": profile["username"],
            }
            social_networks.append(social_network)

        return social_networks

    def format_education(self, education):
        return [
            {
                "institution": edu["institution"],
                "area": edu["area"],
                "degree": edu["studyType"],
                "start_date": edu["startDate"],
                "end_date": edu.get("endDate", "present"),
                "highlights": edu.get("courses", []),
            }
            for edu in education
        ]

    def format_experience(self, work):
        formatted_work = []
        for job in work:
            experience = {
                "company": job["name"],
                "position": job["position"],
                "start_date": job["startDate"],
                "end_date": job.get("endDate", "present"),
                "highlights": job.get("highlights", []),
            }
            if job.get("location"):
                experience["location"] = job["location"]
            formatted_work.append(experience)
        return formatted_work

    def format_publications(self, publications):
        optional_fields = ["doi", "url"]
        formatted_publications = []
        for pub in publications:
            formatted_publication = {
                "title": pub["name"],
                "authors": pub.get("authors", []),
                "date": pub["releaseDate"],
            }

            for optional_field in optional_fields:
                if pub.get(optional_field):
                    formatted_publication[optional_field] = pub[optional_field]

            formatted_publications.append(formatted_publication)

        return formatted_publications

    def format_projects(self, projects):
        formatted_projects = []
        for proj in projects:
            project = {"name": proj["name"]}
            if proj.get("startDate"):
                project["date"] = proj["startDate"]
            if "description" in proj:
                project["highlights"] = [proj["description"]]
            formatted_projects.append(project)
        return formatted_projects

    def format_awards(self, awards):
        return [
            {"label": award["title"], "details": award["awarder"]} for award in awards
        ]

    def format_technologies(self, skills):
        languages = next(
            (skill["keywords"] for skill in skills if skill["name"] == "Languages"), []
        )
        software = next(
            (skill["keywords"] for skill in skills if skill["name"] == "Software"), []
        )
        return [
            {"label": "Languages", "details": ", ".join(languages)},
            {"label": "Software", "details": ", ".join(software)},
        ]

    def convert(self):
        return yaml.dump(self.render_cv, sort_keys=False)


def convert(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        if input_file.endswith(".json"):
            json_resume = json.load(infile)
        elif input_file.endswith(".yaml") or input_file.endswith(".yml"):
            json_resume = yaml.safe_load(infile)
        else:
            print("Unsupported file format. Please provide a .json or .yaml file.")
            sys.exit(1)

    # Validate the input JSON against the JSON Resume schema
    input_validator = SchemaValidator(JSON_RESUME_SCHEMA_URL, "Input JSON Resume")
    input_validator.validate_json(json_resume)

    converter = JSONResumeConverter(json_resume)
    yaml_output = converter.convert()

    # Validate the output YAML against the RenderCV schema
    output_validator = SchemaValidator(RENDER_CV_SCHEMA_URL, "Output RenderCV")
    render_cv_data = yaml.safe_load(yaml_output)
    output_validator.validate_yaml(render_cv_data)

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(yaml_output)


def main():
    if len(sys.argv) != 3:
        print("Usage: jsonresume_to_rendercv resume-schema.json resume-RenderCV.yaml")
        print("Usage: jsonresume_to_rendercv resume-schema.yaml resume-RenderCV.yaml")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert(input_file, output_file)


if __name__ == "__main__":
    main()
