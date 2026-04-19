from src.api import ApiClient
from src.api.models.project import ProjectsResponse, Project


class TestGetProjects:
    def test_get_projects_returns_response(self, api_client: ApiClient):
        """Test that get_projects returns ProjectsResponse."""
        response = api_client.get_projects()

        assert response is not None
        assert isinstance(response, ProjectsResponse)

    def test_get_projects_returns_list_of_projects(self, api_client: ApiClient):
        """Test that projects data is a list of Project objects."""
        response = api_client.get_projects()

        assert isinstance(response.data, list)
        if len(response) > 0:
            assert isinstance(response[0], Project)

    def test_project_has_required_attributes(self, api_client: ApiClient):
        """Test that each project has required attributes."""
        response = api_client.get_projects()

        if len(response) > 0:
            project = response[0]
            assert project.id is not None
            assert project.type == "project"
            assert project.title is not None
            assert project.status is not None

    def test_projects_response_is_iterable(self, api_client: ApiClient):
        """Test that ProjectsResponse can be iterated."""
        projects = api_client.get_projects()

        for project in projects:
            print(f"{project.title} - {project.status}")
            print(f"Tests: {project.tests_count}")
            print(f"URL: {project.attributes.testomatio_url}")
