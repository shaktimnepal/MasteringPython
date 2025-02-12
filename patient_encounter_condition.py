#THIS IS THE WORKING INTER-LINKED PATIENT, ENCOUNTER AND CONDITION DATA GENERATOR


from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.address import Address
from fhir.resources.attachment import Attachment



from fhir.resources.encounter import Encounter

import uuid
import os
import json
import random
from random import randint
from datetime import date, timedelta
from faker import Faker

from fhir.resources.condition import Condition
from fhir.resources.identifier import Identifier
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.period import Period
from fhir.resources.duration import Duration


# Initialize Faker
fake = Faker()

# Define file paths
desktop_path = os.path.expanduser("~/Desktop")
output_folder = os.path.join(desktop_path, "project_json/data_set5/raw_json")
os.makedirs(output_folder, exist_ok=True)
output_file_patient = os.path.join(output_folder, "patients.json")
output_file_encounter = os.path.join(output_folder, "encounters.json")
output_file_condition = os.path.join(output_folder, "conditions.json")

def default_serializer(obj):
    """Custom serializer for non-serializable objects."""

    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def generate_patient_data():
    """Generate a unique FHIR-compliant Patient resource."""

    patient_id = fake.uuid4()  # Unique ID for each patient

    # Generate birthday ensuring person is between 0 and 100 years old
    birthday = fake.date_of_birth(minimum_age=0, maximum_age=100)

    # Today's date
    today = date.today()

    # Function to generate valid start and end times
    def generate_valid_timeframes(start_reference):
        """Generate start and end times ensuring end_time does not exceed today."""
        max_start_time_offset = min(3650, (today - start_reference).days)  # Ensure within range
        start_time = start_reference + timedelta(days=randint(1, max_start_time_offset))

        max_end_time_offset = (today - start_time).days  # Max days possible until today

        # Ensure end_time is between start_time and today
        end_time = start_time + timedelta(days=randint(0, max_end_time_offset))  # Can be same day

        return start_time, end_time

    # Generate valid timeframes for different attributes
    human_name_start_time, human_name_end_time = generate_valid_timeframes(birthday)
    telecom_start_time, telecom_end_time = generate_valid_timeframes(birthday)
    address_start_time, address_end_time = generate_valid_timeframes(birthday)
    contact_start_time, contact_end_time = generate_valid_timeframes(birthday)

    # Determine the latest end date
    latest_end_date = max(human_name_end_time, telecom_end_time, address_end_time, contact_end_time)

    # Generate deceased date ensuring it's after the latest end date but not beyond today
    #min_deceased_offset = (latest_end_date - birthday).days  # Ensure it comes after all end dates
    max_deceased_offset = (today - latest_end_date).days  # Max days possible until today

    # Ensure deceased date is valid
    if max_deceased_offset < 0:
        deceased_date_time1 = latest_end_date  # If today is before latest_end_date, use latest_end_date
    else:
        deceased_date_time1 = latest_end_date + timedelta(days=randint(0, max_deceased_offset))

    # Logic for generating deceasedBoolean and deceasedDateTime
    def generate_deceased_data():
        """Generate deceasedBoolean and deceasedDateTime."""
        deceased_boolean = fake.boolean(chance_of_getting_true=10)  # 10% chance of being True
        deceased_date_time = None

        if deceased_boolean:
            deceased_date_time = deceased_date_time1
        return deceased_boolean, deceased_date_time

    # Generate deceased data
    deceased_boolean, deceased_date_time = generate_deceased_data()

    # Generate multipleBirthBoolean with a 5% chance of being True
    multiple_birth_boolean = fake.boolean(chance_of_getting_true=5)

    # Initialize multiple_birth_integer as None
    multiple_birth_integer = None

    # If multipleBirthBoolean is True, generate a multipleBirthInteger
    if multiple_birth_boolean:
        multiple_birth_integer = random.choice([2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,4,5])

    patient = Patient(
        resourceType="Patient",
        id=patient_id,  # Unique patient ID
        identifier=[
            Identifier(
                use="official",
                system="http://hospital.smarthealthit.org",
                value=str(uuid.uuid4())  # Unique identifier
            )
        ],
        active=fake.boolean(),
        name=[
            HumanName(
                use=fake.random_element(["usual", "official", "temp", "nickname", "anonymous", "old", "maiden"]),
                family=fake.last_name(),
                given=[fake.first_name()],
                prefix=[fake.prefix()],
                suffix=[fake.suffix()],
                period=Period(
                    start=human_name_start_time.isoformat(),
                    end=human_name_end_time.isoformat()
                )

            )
        ],
        telecom=[
            ContactPoint(
                system=fake.random_element(["phone", "fax", "email", "pager", "url", "sms", "other"]),
                value=fake.phone_number(),
                use=fake.random_element(["home", "work", "temp", "old", "mobile"]),
                rank=fake.random_element([1, 1, 1, 2, 3, 4]),
                period=Period(
                    start=telecom_start_time.isoformat(),
                    end=telecom_end_time.isoformat(),

                )
            )
        ],
        gender=fake.random_element(["male", "female", "other", "unknown"]),
        birthDate=birthday,
        deceasedBoolean=deceased_boolean if not deceased_date_time else None,
        deceasedDateTime=deceased_date_time,
        address=[
            Address(
                use=fake.random_element(["home", "work", "temp", "old", "billing"]),
                type=fake.random_element(["postal", "physical", "both"]),
                text="Text representation of the address",
                line=[fake.street_address()],
                city=fake.city(),
                state=fake.state_abbr(),
                postalCode=fake.zipcode(),
                country=fake.country(),
                period=Period(
                    start=address_start_time.isoformat(),
                    end=address_end_time.isoformat(),

                )
            )
        ],
        maritalStatus=CodeableConcept(
            text=fake.random_element(
                ["Single", "Married", "Divorced", "Widowed", "Annulled", "Interlocutory", "Legally Separated",
                 "Common Law", "Domestic partner", "Never Married", "unknown"])
        ),
        multipleBirthBoolean=multiple_birth_boolean if not multiple_birth_integer else None,
        multipleBirthInteger=multiple_birth_integer,
        photo=[
            Attachment(
                contentType="image/jpeg",
                language=fake.language_name(),
                # data=fake.random_int(),
                url=fake.image_url(),
                size=fake.random_int(1, 1024),
                # hash=fake.random_int(),
                title=f"Photo of Patient",
                creation=fake.date(),
                height=fake.random_int(1, 1024),
                width=fake.random_int(1, 1024),
                frames=fake.random_int(1, 1024),
                duration=fake.pydecimal(),
                pages=fake.random_int(1, 1024),

            )
        ],
        contact=[
            {
                "relationship": [
                    CodeableConcept(
                        coding=[
                            Coding(
                                system=fake.uri(),
                                version="Version of the system - if applicable",
                                code=fake.random_element(),
                                display="Representation defined by the system",
                                userSelected=fake.boolean()

                            )
                        ],
                        text=fake.random_element(
                            ["Spouse", "Child", "Parent", "Sibling", "Guardian", "Friend", "Other"]),
                    )
                ],
                # role field was removed because of the errors and not being able to fix it
                "name": HumanName(
                    use=fake.random_element(["usual", "official", "temp", "nickname", "anonymous", "old", "maiden"]),
                    # text=f"Text representation of the full name",
                    family=fake.last_name(),
                    given=[fake.first_name()],
                    prefix=[fake.prefix()],
                    suffix=[fake.suffix()],
                    period=Period(
                        start=contact_start_time.isoformat(),
                        end=contact_end_time.isoformat()
                    ),

                ),
                # additionalName not used for the scope of project
                "telecom": [
                    ContactPoint(
                        system=fake.random_element(["phone", "fax", "email", "pager", "url", "sms", "other"]),
                        value=fake.phone_number(),
                        use=fake.random_element(["home", "work", "temp", "old", "mobile"]),
                        rank=fake.random_element([1, 1, 1, 2, 3, 4]),
                        period=Period(
                            start=fake.date(),
                            end=fake.date(),

                        ),
                    ),
                ],
                "address": Address(
                    use=fake.random_element(["home", "work", "temp", "old", "billing"]),
                    type=fake.random_element(["postal", "physical", "both"]),
                    # text="Text representation of the address",
                    line=[fake.street_address()],
                    city=fake.city(),
                    state=fake.state_abbr(),
                    postalCode=fake.zipcode(),
                    country=fake.country(),
                    period=Period(
                        start=fake.date(),
                        end=fake.date(),

                    )
                ),
                # additionalAddress not used
                "gender": fake.random_element(["male", "female", "other", "unknown"]),
                "organization": Reference(
                    display=fake.company()
                ),
                "period": Period(
                    start=fake.date(),
                    end=fake.date(),
                )
            }
        ],
        communication=[
            {
                "language": CodeableConcept(
                    text=fake.language_name()
                ),
                "preferred": fake.boolean()
            }
        ],
        generalPractitioner=[
            Reference(
                display=f"Dr. {fake.last_name()} {fake.first_name()}"
            )
        ],
        managingOrganization=Reference(
            display=fake.company()
        )
    )

    return birthday, today, deceased_date_time, patient_id, patient.model_dump()  # Return both patient ID and JSON data

######### Here begins the Encounter Resource

CLASS_CODING = [
    {'code': 'IMP', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode', 'display': 'inpatient encounter'},
    {'code': 'AMB', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode','display': 'ambulatory'},
    {'code': 'OBSENC', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode', 'display': 'observation encounter'},
    {'code': 'EMER', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode', 'display': 'emergency'},
    {'code': 'VR', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode', 'display': 'virtual'},
    {'code': 'HH', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActCode', 'display': 'home health'},

]
PRIORITY = [
    {'code': 'A', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActPriority', 'display': 'ASAP'},
    {'code': 'CR', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActPriority','display': 'callback results'},
    {'code': 'EL', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActPriority', 'display': 'elective'},
    {'code': 'EM', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActPriority', 'display': 'emergency'},
    {'code': 'P', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActPriority', 'display': 'preop'},
    {'code': 'PRN', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActPriority', 'display': 'as needed'},
    {'code': 'R', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ActPriority', 'display': 'routine'},

]
TYPE = [
    {'code': 'ADMS', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-type', 'display': 'Annual diabetes mellitus screening'},
    {'code': 'BD/BM-clin', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-type', 'display': 'Bone drilling/bone marrow punction in clinic'},
    {'code': 'CCS60', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-type', 'display': 'Infant colon screening - 60 minutes'},
    {'code': 'OKI', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-type', 'display': 'Outpatient Kenacort injection'}

]

SERVICE_TYPE = [
    {'code': '1', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Adoption & permanent care information/support'},
    {'code': '2', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Aged care assessment'},
    {'code': '3', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Aged Care information/referral'},
    {'code': '4', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Aged Residential Care'},
    {'code': '5', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Case management for older persons'},
    {'code': '6', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Delivered meals (meals on wheels)'},
    {'code': '7', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Friendly visiting'},
    {'code': '8', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Home care/housekeeping assistance'},
    {'code': '9', 'system': 'http://terminology.hl7.org/CodeSystem/service-type', 'display': 'Home maintenance and repair'},

]
SUBJECT_STATUS = [
    {'code': 'arrived', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-subject-status', 'display': 'Arrived'},
    {'code': 'triaged', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-subject-status', 'display': 'Triaged'},
    {'code': 'receiving-care', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-subject-status', 'display': 'Receiving Care'},
    {'code': 'on-leave', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-subject-status', 'display': 'On Leave'},
    {'code': 'departed', 'system': 'http://terminology.hl7.org/CodeSystem/encounter-subject-status', 'display': 'Departed'}

]
PARTICIPANT_TYPE = [
    {'code': 'ADM', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ParticipationType', 'display': 'admitter'},
    {'code': 'ATND', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ParticipationType', 'display': 'attender'},
    {'code': 'CALLBCK', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ParticipationType', 'display': 'callback contact'},
    {'code': 'CON', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ParticipationType', 'display': 'consultant'},
    {'code': 'DIS', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ParticipationType', 'display': 'discharger'},
    {'code': 'ESC', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ParticipationType', 'display': 'escort'},
    {'code': 'REF', 'system': 'http://terminology.hl7.org/CodeSystem/v3-ParticipationType', 'display': 'referrer'},
    {'code': 'translator', 'system': 'http://terminology.hl7.org/CodeSystem/participant-type', 'display': 'Translator'},
    {'code': 'emergency', 'system': 'http://terminology.hl7.org/CodeSystem/participant-type', 'display': 'Emergency'},

]
DIAGNOSIS_USE = [
    {'code': 'working', 'system': 'http://hl7.org/fhir/encounter-diagnosis-use', 'display': 'Working'},
    {'code': 'final', 'system': 'http://hl7.org/fhir/encounter-diagnosis-use', 'display': 'Final'},
]

DIAGNOSIS_CONDITION = [
    {'code': '404684003', 'system': 'http://snomed.info/sct', 'display': 'Clinical finding (finding)'},
    {'code': '109006', 'system': 'http://snomed.info/sct', 'display': 'Anxiety disorder of childhood OR adolescence'},
    {'code': '122003', 'system': 'http://snomed.info/sct', 'display': 'Choroidal hemorrhage'},
    {'code': '127009', 'system': 'http://snomed.info/sct', 'display': 'Spontaneous abortion with laceration of cervix'},
    {'code': '129007', 'system': 'http://snomed.info/sct', 'display': 'Homoiothermia'},
    {'code': '134006', 'system': 'http://snomed.info/sct', 'display': 'Decreased hair growth'},
    {'code': '140004', 'system': 'http://snomed.info/sct', 'display': 'Chronic pharyngitis'},
    {'code': '144008', 'system': 'http://snomed.info/sct', 'display': 'Normal peripheral vision'},
    {'code': '150003', 'system': 'http://snomed.info/sct', 'display': 'Abnormal bladder continence'},

]
DIET_PREFERENCE = [
    {'code': 'vegetarian', 'system': 'http://terminology.hl7.org/CodeSystem/diet', 'display': 'Vegetarian'},
    {'code': 'dairy-free', 'system': 'http://terminology.hl7.org/CodeSystem/diet', 'display': 'Dairy Free'},
    {'code': 'nut-free', 'system': 'http://terminology.hl7.org/CodeSystem/diet', 'display': 'Nut Free'},
    {'code': 'gluten-free', 'system': 'http://terminology.hl7.org/CodeSystem/diet', 'display': 'Gluten Free'},
    {'code': 'vegan', 'system': 'http://terminology.hl7.org/CodeSystem/diet', 'display': 'Vegan'},
    {'code': 'halal', 'system': 'http://terminology.hl7.org/CodeSystem/diet', 'display': 'Halal'},
    {'code': 'kosher', 'system': 'http://terminology.hl7.org/CodeSystem/diet', 'display': 'Kosher'}

]
ADMIT_SOURCE = [
    {'code': 'hosp-trans', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'Transferred from other hospital'},
    {'code': 'emd', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'From accident/emergency department'},
    {'code': 'outp', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'From outpatient department'},
    {'code': 'born', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'Born in hospital'},
    {'code': 'gp', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'General Practitioner referral'},
    {'code': 'mp', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'Medical Practitioner/physician referral'},
    {'code': 'nursing', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'From nursing home'},
    {'code': 'psych', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'From psychiatric hospital'},
    {'code': 'rehab', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'From rehabilitation facility'},
    {'code': 'other', 'system': 'http://terminology.hl7.org/CodeSystem/admit-source', 'display': 'Other'},
]
DISCHARGE_DISPOSITION = [
    {'code': 'home', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Home'},
    {'code': 'alt-home', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Alternative home'},
    {'code': 'other-hcf', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Other healthcare facility'},
    {'code': 'hosp', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Hospice'},
    {'code': 'long', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Long-term care'},
    {'code': 'aadvice', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Left against advice'},
    {'code': 'exp', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Expired'},
    {'code': 'psy', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Psychiatric hospital'},
    {'code': 'rehab', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Rehabilitation'},
    {'code': 'snf', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Skilled nursing facility'},
    {'code': 'oth', 'system': 'http://terminology.hl7.org/CodeSystem/discharge-disposition', 'display': 'Other'},

]
def generate_encounter_data(birthday, today, deceased_date_time, patient_id, encounter_start_min_date):
    """Generate a unique FHIR-compliant Encounter resource linked to a patient."""

    encounter_id = fake.uuid4()  # Unique encounter ID

    class_choice = random.choice(CLASS_CODING)
    priority_choice = random.choice(PRIORITY)
    type_choice = random.choice(TYPE)
    service_type_choice = random.choice(SERVICE_TYPE)
    subject_status_choice = random.choice(SUBJECT_STATUS)
    participant_type_choice = random.choice(PARTICIPANT_TYPE)
    diagnosis_use_choice1 = random.choice(DIAGNOSIS_USE)
    diagnosis_use_choice2 = random.choice(DIAGNOSIS_USE)
    diagnosis_use_choice3 = random.choice(DIAGNOSIS_USE)
    diagnosis_condition_choice1 = random.choice(DIAGNOSIS_CONDITION)
    diagnosis_condition_choice2 = random.choice(DIAGNOSIS_CONDITION)
    diagnosis_condition_choice3 = random.choice(DIAGNOSIS_CONDITION)
    diet_preference_choice = random.choice(DIET_PREFERENCE)
    admit_source_choice = random.choice(ADMIT_SOURCE)
    discharge_disposition_choice = random.choice(DISCHARGE_DISPOSITION)

    # Function to ensure a date range is between birthday and deceased_date_time (if exists)
    def generate_valid_event_timeframes(birthday, today, deceased_date_time=None, encounter_start_min_date=None):
        """Ensure participant and actual and planned encounter times are valid within birthday and deceased date (if applicable)."""

        max_valid_end_date = deceased_date_time if deceased_date_time else today

        # Ensure first encounter does not go too far back and encounter start time is within valid range
        if encounter_start_min_date is None:
            encounter_start_min_date = max(birthday, today - timedelta(days=375))
        encounter_start_max_date = min(max_valid_end_date, today - timedelta(days=10))

        # Ensure the date range is valid
        if encounter_start_min_date > encounter_start_max_date:
            encounter_start_min_date = encounter_start_max_date  # Prevents invalid range

        actual_encounter_start_time = fake.date_between(start_date=encounter_start_min_date,
                                                        end_date=encounter_start_max_date)

        # Ensure encounter end time follows start time
        actual_encounter_end_time = actual_encounter_start_time + timedelta(days=randint(1, 10))

        # Calculate encounter length
        actual_encounter_length = (actual_encounter_end_time - actual_encounter_start_time).days

        return  actual_encounter_start_time, actual_encounter_end_time, actual_encounter_length

    # Generate participant and encounter timeframes
    actual_encounter_start_time, actual_encounter_end_time, actual_encounter_length = generate_valid_event_timeframes(birthday, today, deceased_date_time, encounter_start_min_date)
    participant_start_time = (actual_encounter_start_time + timedelta(days=randint(1, 3)))
    participant_end_time = (participant_start_time + timedelta(days=randint(1, 6)))
    planned_start_date = (actual_encounter_start_time + timedelta(days=randint(-3, 3)))
    planned_end_date = (planned_start_date + timedelta(days=randint(0, 6)))


    encounter = Encounter(
        resourceType="Encounter",
        id=encounter_id,  # Unique encounter ID
        identifier=[
            Identifier(
                use="official",
                system="http://hospital.smarthealthit.org",
                value=encounter_id  # Unique identifier
            )
        ],
        status=random.choice(["planned", "in-progress", "on-hold", "discharged", "completed", "cancelled", "discontinued", "entered-in-error", "unknown"]),
        class_fhir=[{
            "coding": [Coding(
                system=class_choice["system"],
                code=class_choice["code"],
                display=class_choice["display"]
            )]
        }],
        priority=CodeableConcept(
            coding=[Coding(
                system=priority_choice["system"],
                code=priority_choice["code"],
                display=priority_choice["display"]
            )]
        ),
        type=[CodeableConcept(
            coding=[Coding(
                system=type_choice["system"],
                code=type_choice["code"],
                display=type_choice["display"]
            )]
        )],
        serviceType=[
            CodeableReference(
                concept=CodeableConcept(
                    coding=[
                        Coding(
                            system=service_type_choice["system"],
                            code=service_type_choice["code"],
                            display=service_type_choice["display"]
                        )
                    ]
                )
            )
        ],
        subject=Reference(
            reference=f"{patient_id}",
            #display=fake.name()
        ),
        subjectStatus=CodeableConcept(
            coding=[Coding(
                system=subject_status_choice["system"],
                code=subject_status_choice["code"],
                display=subject_status_choice["display"]
            )]
        ),
        episodeOfCare=[Reference(
            reference=f"EpisodeOfCare/{fake.name()}",
            type=fake.uri(),
            display=f"This is episode number {fake.random_int(1, 10)} of care"
        )
        ],
        basedOn=[Reference(
            reference=f'{random.choice(["CarePlan", "DeviceRequest", "ImmunizationRecommendation", "MedicationRequest", "NutritionOrder", "RequestOrchestration", "ServiceRequest", "VisionPrescription"])} initiated this encounter',
        )
        ],
        careTeam=[
            Reference(
                reference=f"The group led by Dr. {fake.name()} is allocated to participate in this encounter"
            )
        ],
        partOf=Reference(
            reference=f"This Encounter is part of another encounter: {fake.uuid4()}"
        ),
        serviceProvider=Reference(
            reference=random.choice(
                ["Emergency", "Surgery", "Cardiology", "Pediatrics", "Oncology", "Neurology", "ICU", "ENT"])
        ),
        participant=[{
            "type": [CodeableConcept(
                coding=[Coding(
                    system=participant_type_choice["system"],
                    code=participant_type_choice["code"],
                    display=participant_type_choice["display"]
                )]
            )],
            "period": Period(
                start=participant_start_time.isoformat(),
                end=participant_end_time.isoformat()
            ),
            "actor": Reference(
                reference=f"Practitioner/{fake.uuid4()}")
        }],
        appointment=[Reference(
            reference=f"Appointment that scheduled this encounter/{fake.uuid4()}"
        )],

        actualPeriod=Period(
            start=actual_encounter_start_time.isoformat(),
            end=actual_encounter_end_time.isoformat()
        ),
        plannedStartDate=planned_start_date.isoformat(),
        plannedEndDate=planned_end_date.isoformat(),
        length=Duration(
            value=actual_encounter_length,
            unit="days"
        ),

        reason=[{
            "value": [{
                "concept": {
                    "text": fake.sentence()
                }
            }]
        }],
        diagnosis=[
            {
                "condition": [{
                    "concept": {
                        "coding": [Coding(
                            system=diagnosis_condition_choice1["system"],
                            code=diagnosis_condition_choice1["code"],
                            display=diagnosis_condition_choice1["display"]
                        )

                        ]
                    },
                    "reference": {
                        "reference": f"Condition/{fake.uuid4()}"
                    }
                }],
                "use": [CodeableConcept(
                    coding=[Coding(
                        system=diagnosis_use_choice1["system"],
                        code=diagnosis_use_choice1["code"],
                        display=diagnosis_use_choice1["display"]
                    )]
                )]
            },
            {
                "condition": [{
                    "concept": {
                        "coding": [Coding(
                            system=diagnosis_condition_choice2["system"],
                            code=diagnosis_condition_choice2["code"],
                            display=diagnosis_condition_choice2["display"]
                        )

                        ]
                    },
                    "reference": {
                        "reference": f"Condition/{fake.uuid4()}"
                    }
                }],
                "use": [CodeableConcept(
                    coding=[Coding(
                        system=diagnosis_use_choice2["system"],
                        code=diagnosis_use_choice2["code"],
                        display=diagnosis_use_choice2["display"]
                    )]
                )]
            },
            {
                "condition": [{
                    "concept": {
                        "coding": [Coding(
                            system=diagnosis_condition_choice3["system"],
                            code=diagnosis_condition_choice3["code"],
                            display=diagnosis_condition_choice3["display"]
                        )

                        ]
                    },
                    "reference": {
                        "reference": f"Condition/{fake.uuid4()}"
                    }
                }],
                "use": [CodeableConcept(
                    coding=[Coding(
                        system=diagnosis_use_choice3["system"],
                        code=diagnosis_use_choice3["code"],
                        display=diagnosis_use_choice3["display"]
                    )]
                )]
            }

        ],
        account=[Reference(
            reference=f"Account/{fake.name()}"
        )],
        dietPreference=[CodeableConcept(
            coding=[Coding(
                system=diet_preference_choice["system"],
                code=diet_preference_choice["code"],
                display=diet_preference_choice["display"]
            )]
        )],
        specialArrangement=[CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/encounter-special-arrangements",
                code=random.choice(["1", "2", "3", "4", "5"]),
                display=random.choice(["Wheelchair", "Additional bedding", "Interpreter", "Attendant", "Guide dog"])
            )]
        )],
        specialCourtesy=[CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/encounter-special-arrangements",
                code=random.choice(["1", "2", "3", "4", "5", "6"]),
                display=random.choice(["extended courtesy", "normal courtesy", "professional courtesy", "staff", "very important person", "unknown"])
            )]
        )],
        admission={
            "origin": Reference(
                reference=f"{fake.first_name()} Medical Center, {fake.address()}"
            ),
            "admitSource": CodeableConcept(
                coding=[Coding(
                    system=admit_source_choice["system"],
                    code=admit_source_choice["code"],
                    display=admit_source_choice["display"]
                )]
            ),
            "reAdmission": CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0092",
                    code=f"{fake.boolean(15)}",
                    display="Re-admission"
                )]
            ),
            "destination": Reference(
                reference=f"{fake.last_name()} Treatment Center, {fake.address()}"
            ),
            "dischargeDisposition": CodeableConcept(
                coding=[Coding(
                    system=discharge_disposition_choice["system"],
                    code=discharge_disposition_choice["code"],
                    display=discharge_disposition_choice["display"]
                )]
            )
        }

    )

    return encounter_id, actual_encounter_end_time, encounter.model_dump()

############ Here starts the Condition Resource

CLINICAL_STATUS = [
    {'code': 'active', 'level': '1', 'display': 'Active'},
    {'code': 'recurrence', 'level': '2', 'display': 'Recurrence'},
    {'code': 'relapse', 'level': '2', 'display': 'Relapse'},
    {'code': 'inactive', 'level': '1', 'display': 'Inactive'},
    {'code': 'remission', 'level': '2', 'display': 'Remission'},
    {'code': 'resolved', 'level': '2', 'display': 'Resolved'},
    {'code': 'unknown', 'level': '1', 'display': 'Unknown'},
]
VERIFICATION_STATUS = [
    {'code': 'unconfirmed', 'level': '1', 'display': 'Unconfirmed'},
    {'code': 'provisional', 'level': '2', 'display': 'Provisional'},
    {'code': 'differential', 'level': '2', 'display': 'Differential'},
    {'code': 'confirmed', 'level': '1', 'display': 'Confirmed'},
    {'code': 'refuted', 'level': '1', 'display': 'Refuted'},
    {'code': 'entered-in-error', 'level': '1', 'display': 'Entered in Error'},
]

CATEGORY = [
    {'code': 'problem-list-item', 'display': 'Problem List I tem'},
    {'code': 'encounter-diagnosis', 'display': 'Encounter Diagnosis'}
]

SEVERITY = [
    {'code': '24484000', 'display': 'Severe'},
    {'code': '6736007', 'display': 'Moderate'},
    {'code': '255604002', 'display': 'Mild'}
]

CODE = [
    {'code': '404684003', 'system': 'http://snomed.info/sct', 'display': 'Clinical finding (finding)'},
    {'code': '109006', 'system': 'http://snomed.info/sct', 'display': 'Anxiety disorder of childhood OR adolescence'},
    {'code': '122003', 'system': 'http://snomed.info/sct', 'display': 'Choroidal hemorrhage'},
    {'code': '127009', 'system': 'http://snomed.info/sct', 'display': 'Spontaneous abortion with laceration of cervix'},
    {'code': '129007', 'system': 'http://snomed.info/sct', 'display': 'Homoiothermia'},
    {'code': '134006', 'system': 'http://snomed.info/sct', 'display': 'Decreased hair growth'},
    {'code': '140004', 'system': 'http://snomed.info/sct', 'display': 'Chronic pharyngitis'},
    {'code': '144008', 'system': 'http://snomed.info/sct', 'display': 'Normal peripheral vision'},
    {'code': '150003', 'system': 'http://snomed.info/sct', 'display': 'Abnormal bladder continence'},

]

BODY_SITE = [
    {'code': '53075003', 'display': 'Distal phalanx of hallux'},
    {'code': '3055008', 'display': 'Bone marrow of vertebral body'},
    {'code': '3964001', 'display': 'Gyrus of brain'},
    {'code': '344001', 'display': 'Ankle'},
    {'code': '691000', 'display': 'Small intestine submucosa'},
    {'code': '688000', 'display': 'Fetal hyaloid artery'},
    {'code': '4703008', 'display': 'Cardinal vein'},
    {'code': '5597008', 'display': 'Retina of right eye'},
    {'code': '7242000', 'display': 'Appendiceal muscularis propria'},
    {'code': '7756004', 'display': 'Lamina of third thoracic vertebra'},
    {'code': '8711009', 'display': 'Periodontal tissues'},
    {'code': '9796009', 'display': 'Skeletal muscle fiber, type IIb'}
]

PARTICIPANT_FUNCTION = [
    {'code': 'enterer', 'display': 'Enterer'},
    {'code': 'performer', 'display': 'Performer'},
    {'code': 'author', 'display': 'Author'},
    {'code': 'verifier', 'display': 'Verifier'},
    {'code': 'legal', 'display': 'Legal Authenticator'},
    {'code': 'attester', 'display': 'Attester'}
]

STAGE_SUMMARY = [
    {'code': '385356007', 'display': 'Tumor stage finding (finding)'},
    {'code': '2640006', 'display': 'Clinical stage IV'},
    {'code': '56769006', 'display': 'Modified Dukes stage A'},
    {'code': '385368003', 'display': 'FIGO stage finding for cervical carcinoma'},
    {'code': '394940002', 'display': 'Dukes stage B (finding)'},
    {'code': '396907008', 'display': 'Thymic epithelial neoplasm stage finding (finding)'},
    {'code': '405917009', 'display': 'Intergroup rhabdomyosarcoma study post-surgical clinical group finding (finding)'},
    {'code': '50283003', 'display': 'Clinical stage III'},
    {'code': '277772008', 'display': 'Node stage N1bi'},
    {'code': '53623008', 'display': 'N1 stage'}
]

STAGE_TYPE = [
    {'code': '261023001', 'display': 'Pathological staging (qualifier value)'},
    {'code': '260998006', 'display': 'Clinical staging (qualifier value)'},
    {'code': '254291000', 'display': 'Staging and scales'},
    {'code': '13808002', 'display': 'WR stage 3'},
    {'code': '134438001', 'display': 'Canadian Cardiovascular Society classification of angina'},
    {'code': '165270003', 'display': 'Physical disability assessment score'},
    {'code': '251896001', 'display': 'Breathlessness rating'},
    {'code': '254365003', 'display': 'Siopel liver staging system'},
    {'code': '254376004', 'display': 'Testicular tumor staging systems'},
    {'code': '258233007', 'display': 'Generic tumor staging descriptor (tumor staging)'}
]

def generate_condition(birthday,today, deceased_date_time, patient_id, encounter_id):

    condition_id = fake.uuid4()

    clinical_status_choice = random.choice(CLINICAL_STATUS)
    verification_status_choice = random.choice(VERIFICATION_STATUS)
    category_choice = random.choice(CATEGORY)
    severity_choice = random.choice(SEVERITY)
    code_choice = random.choice(CODE)
    body_site_choice = random.choice(BODY_SITE)
    participant_function_choice = random.choice(PARTICIPANT_FUNCTION)
    stage_summary_choice = random.choice(STAGE_SUMMARY)
    stage_type_choice = random.choice(STAGE_TYPE)

    def generate_condition_dates(birthday, today, deceased_date_time=None):
        """Generate valid onset, abatement, and recorded dates within birthday and deceased date (if applicable)."""

        max_valid_end_date = deceased_date_time if deceased_date_time else today

        # Ensure onset_date_time is within the valid range
        min_onset_offset = 3650  # Minimum 10 years after birthday
        max_onset_offset = min(18000, (max_valid_end_date - birthday).days)

        if min_onset_offset > max_onset_offset:
            onset_date_time = birthday  # If range is invalid, default to birthday
        else:
            onset_date_time = birthday + timedelta(days=randint(min_onset_offset, max_onset_offset))

        # Ensure abatement_date_time follows onset_date_time
        min_abatement_offset = 365  # Minimum 1 year after onset_date_time
        max_abatement_offset = min(3650, (max_valid_end_date - onset_date_time).days)

        if min_abatement_offset > max_abatement_offset:
            abatement_date_time = onset_date_time  # Default to onset_date_time if range is invalid
        else:
            abatement_date_time = onset_date_time + timedelta(days=randint(min_abatement_offset, max_abatement_offset))

        # Ensure recorded_date_time follows onset_date_time but is before abatement_date_time
        min_recorded_offset = 1  # Minimum 1 day after onset
        max_recorded_offset = min(364, (abatement_date_time - onset_date_time).days)

        if min_recorded_offset > max_recorded_offset:
            recorded_date_time = onset_date_time  # Default to onset_date_time if range is invalid
        else:
            recorded_date_time = onset_date_time + timedelta(days=randint(min_recorded_offset, max_recorded_offset))

        return onset_date_time, abatement_date_time, recorded_date_time

    onset_date_time, abatement_date_time, recorded_date_time = generate_condition_dates(birthday, today, deceased_date_time)

    condition = Condition(
        resourceType="Condition",
        id=condition_id,
        identifier=[
            Identifier(
                use="official",
                system="http://hospital.smarthealthit.org",
                value=condition_id
            )
        ],
        clinicalStatus=CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/condition-clinical",
                version=f'Level: {clinical_status_choice["level"]}',
                code=clinical_status_choice["code"],
                display=clinical_status_choice["display"],

            )]
        ),
        verificationStatus=CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/condition-ver-status",
                version=f'Level: {verification_status_choice["level"]}',
                code=verification_status_choice["code"],
                display=verification_status_choice["display"],
            )]
        ),
        category=[CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/condition-category",
                code=category_choice["code"],
                display=category_choice["display"]
            )]
        )],
        severity=CodeableConcept(
            coding=[Coding(
                system="http://snomed.info/sct",
                code=severity_choice["code"],
                display=severity_choice["display"]
            )],
        ),
        code=CodeableConcept(
            coding=[Coding(
                system=code_choice["system"],
                code=code_choice["code"],
                display=code_choice["display"]
            )],
        ),
        bodySite=[CodeableConcept(
            coding=[Coding(
                system="http://snomed.info/sct",
                code=body_site_choice["code"],
                display=body_site_choice["display"]
            )]
        )],
        subject=Reference(
            reference=f"{patient_id}",
            #display="Patient Name"
        ),
        encounter=Reference(
            reference=f"{encounter_id}",
            display="Fake encounter id associated with this condition"
        ),
        onsetDateTime=onset_date_time.isoformat(),
        abatementDateTime=abatement_date_time.isoformat(),
        recordedDate=recorded_date_time.isoformat(),
        participant=[{
            "function": CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                    code=participant_function_choice["code"],
                    display=participant_function_choice["display"]
                )]
            ),
            "actor": Reference(
                reference=f"Practitioner/Dr. {fake.name()}")
        }],
        stage=[{
            "summary": CodeableConcept(
                coding=[Coding(
                    system="http://snomed.info/sct",
                    code=stage_summary_choice["code"],
                    display=stage_summary_choice["display"]
                )]
            ),
            "type": CodeableConcept(
                coding=[Coding(
                    system="http://snomed.info/sct	",
                    code=stage_type_choice["code"],
                    display=stage_type_choice["display"]
                )]
            ),

        }]
    )
    return condition.model_dump()

# Generate n patient records and their encounters
patients = []
encounters = []
conditions = []

for _ in range(10000):
    birthday, today, deceased_date_time, patient_id, patient_data = generate_patient_data()  # Generate a unique patient
    patients.append(patient_data)

    # Start encounter tracking from the patient's birthday
    encounter_start_min_date = None

    # Generate 1 to 5 encounters per patient
    for _ in range(random.choice([1,1,1,1,1,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,5,5])):
        encounter_id, last_encounter_end_date, encounter_data = generate_encounter_data(birthday, today, deceased_date_time, patient_id, encounter_start_min_date)
        encounters.append(encounter_data)
        # Ensure the next encounter starts after this one
        encounter_start_min_date = last_encounter_end_date

        # Generate 1 to 3 conditions per encounter of patients
        for _ in range(randint(1, 3)):
            conditions.append(generate_condition(birthday, today, deceased_date_time, patient_id, encounter_id))


# Save to JSON file
with open(output_file_patient, "w") as f:
    json.dump(patients, f, indent=4, default=default_serializer)

print(f" Patient records saved at: {output_file_patient}")

# Save encounters to JSON file
with open(output_file_encounter, "w") as f:
    json.dump(encounters, f, indent=4)

print(f" Encounter records saved at: {output_file_encounter}")

# Save encounters to JSON file
with open(output_file_condition, "w") as f:
    json.dump(conditions, f, indent=4)

print(f" Condition records saved at: {output_file_condition}")
