import instructor
from openai import OpenAI
from models import Profile, Address

class ProfileExtractor:
    def __init__(self, openai_api_key: str):
        self.client = instructor.patch(OpenAI(api_key=openai_api_key))

    def extract_profile_info(self, text: str, current_profile: Profile) -> Profile:
        """Extract profile information from text and update the current profile"""
        prompt = f"""
        Extract profile information from the following text. Only update fields that are mentioned in the text.
        Current profile information:
        {current_profile.model_dump_json(indent=2)}
        
        Text to analyze:
        {text}
        """
        
        try:
            updated_profile = self.client.chat.completions.create(
                model="gpt-4",
                response_model=Profile,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Merge the updated profile with the current profile
            merged_profile = Profile(
                name=updated_profile.name or current_profile.name,
                gender=updated_profile.gender or current_profile.gender,
                age=updated_profile.age or current_profile.age,
                mobile_number=updated_profile.mobile_number or current_profile.mobile_number,
                email=updated_profile.email or current_profile.email,
                address=Address(
                    state=updated_profile.address.state or current_profile.address.state,
                    city=updated_profile.address.city or current_profile.address.city,
                    zipcode=updated_profile.address.zipcode or current_profile.address.zipcode,
                    location=updated_profile.address.location or current_profile.address.location,
                    building_name=updated_profile.address.building_name or current_profile.address.building_name,
                    house_number=updated_profile.address.house_number or current_profile.address.house_number
                )
            )
            
            return merged_profile
        except Exception as e:
            print(f"Error in profile extraction: {e}")
            return current_profile 