"""
Generates the API spec in openAPI3 format, from the
"""
import json

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import schemas
import blueprints


def generate(app, api_commit_hash):


    
    ###########################
    ##### API SPEC ############
    # API spec is autogenerated using the 'api-spec' library, and saved in the project root
    # as well as being served on the root '/' endpoint for consumption by services
    spec = APISpec(
        title="RCPCH Digital Growth Charts API",
        version=api_commit_hash,
        openapi_version="3.0.2",
        info=dict(
            description="Royal College of Paediatrics and Child Health Digital Growth Charts",
            license={"name": "GNU Affero General Public License",
                     "url": "https://www.gnu.org/licenses/agpl-3.0.en.html"}),
        plugins=[MarshmallowPlugin(), FlaskPlugin()],
        servers=[{"url": 'https://api.rcpch.ac.uk/',
                  "description": 'RCPCH Production API Gateway (subscription keys required)'},
                 {"url": 'https://localhost:5000/',
                  "description": 'Your local development API'}],
    )

    spec.components.schema(
        "uk_who_calculation",
        schema=schemas.CalculationResponseSchema)
    with app.test_request_context():
        spec.path(view=blueprints.uk_who_blueprint.uk_who_calculation)

    spec.components.schema(
        "chartData",
        schema=schemas.ChartDataResponseSchema)
    with app.test_request_context():
        spec.path(
            view=blueprints.uk_who_blueprint.uk_who_chart_coordinates)

    spec.components.schema(
        "plottableChildData",
        schema=schemas.PlottableChildDataResponseSchema)
    with app.test_request_context():
        spec.path(
            view=blueprints.uk_who_blueprint.uk_who_plottable_child_data)

    spec.components.schema(
        "references", schema=schemas.ReferencesResponseSchema)
    with app.test_request_context():
        spec.path(view=blueprints.utilities_blueprint.references)

    # Instructions endpoint (TODO: #121 #120 candidate for deprecation)
    with app.test_request_context():
        spec.path(view=blueprints.utilities_blueprint.instructions)

    # Trisomy 21 endpoint
    spec.components.schema(
        "trisomy_21_calculation",
        schema=schemas.CalculationResponseSchema)
    with app.test_request_context():
        spec.path(view=blueprints.trisomy_21_blueprint.trisomy_21_calculation)
        
    # OpenAPI3 specification endpoint
    with app.test_request_context():
        spec.path(view=blueprints.openapi_blueprint.openapi_endpoint)


    # Turner's syndrome endpoint
    spec.components.schema(
        "turner_calculation",
        schema=schemas.CalculationResponseSchema)
    with app.test_request_context():
        spec.path(view=blueprints.turner_blueprint.turner_calculation)

    ##### END API SPEC ########
    ###########################

    ################################
    ### API SPEC AUTO GENERATION ###

    # Create OpenAPI Spec and serialise it to file
    with open(r'openapi.yml', 'w') as file:
        openapi_yml = file.write(spec.to_yaml())

    with open(r'openapi.json', 'w') as file:
        openapi_json = file.write(json.dumps(
            spec.to_dict(), sort_keys=True, indent=4))
    ### END API SPEC AUTO GENERATION ###
    ####################################

    return spec
