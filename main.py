import argparse
import datetime
import json
import random
import time
import requests
import form

def fill_random_value(type_id, entry_id, options, required=False, entry_name=''):
    ''' Fill random value with a 70% inclination towards positive responses for Cheify and 30% against. '''
    preferred_answers = {
        "entry.65224013": ["Daily", "A few times a week", "Once a week", "Rarely"],
        "entry.258016898": ["Lack of time", "Difficulty in meal planning", "Prefer eating out", "Grocery shopping is inconvenient", "Lack of cooking skills", "Too much food waste"],
        "entry.2010490686": ["Daily", "A few times a week", "Once a week", "Rarely"],
        "entry.1994231910": ["A small family (2-4 people)", "Just myself", "Me and a roommate/partner", "A larger household (5+ people)"],
        "entry.927063382": ["Health & Nutrition", "Cost", "Taste & Variety", "Convenience", "Cooking Skills Required"],
        "entry.1992841976": ["Yes", "No", "Sometimes"],
        "entry.2111463074": ["Frequently", "Occasionally", "Rarely", "Never"],
        "entry.1878407003": ["Yes, I struggle with variety", "Sometimes", "No, I enjoy experimenting"],
        "entry.2079810614": ["Yes, I don’t want to waste or overspend", "Sometimes, if ingredients are costly or rare", "No, I don’t mind buying full packs"],
        "entry.1056370270": ["Very appealing, I would definitely try it", "Somewhat appealing, I might try it", "Neutral, I’m not sure", "Not appealing, I prefer other meal options"],
        "entry.549735418": ["Saves time on grocery shopping", "Helps reduce food waste", "Provides step-by-step cooking guidance", "Offers a variety of new and interesting meals", "Uses fresh and high-quality ingredients", "Fits specific dietary needs (e.g., vegetarian, keto, gluten-free)"],
        "entry.1744218307": ["Essential – I carefully track my food intake and portion sizes", "Somewhat important – I prefer balanced portions but don’t track closely", "Not important – I eat based on hunger and preference"],
        "entry.1219017310": ["Yes, I love customization", "Maybe, depending on the options", "No, I prefer fixed recipes"],
        "entry.901844076": ["Yes, I’d love a hassle-free way to cook fresh meals while traveling", "Maybe, if the meals are easy to prepare and require minimal effort.", "No, I prefer dining out or ordering takeout while travelling"],
        "entry.471915419": ["Supermarkets", "Local vendors", "Online grocery stores", "Meal delivery services", "I don't buy groceries often"],
        "entry.1898577065": ["Both options should be available", "One-time meal kit purchases", "Subscription plan"],
        "entry.641739757": ["Convenience", "Meal variety", "Ingredient quality", "Price", "Portion sizes"],
        "entry.317610989": ["Yes, definitely", "Maybe, if the price and meals fit my needs", "No, I prefer other options"],
        "entry.922951101": ["I would love to see more easy-to-make international cuisines.", "Having options for quick meals that don’t require much prep would be great.", "A good balance between taste and nutrition would be ideal.", "More recipes focused on high-protein diets would be useful."],
        "entry.1056380256": ["More plant-based options would be great!", "A customizable meal plan based on allergies and preferences would be helpful.", "I’d like to see regional dishes from different parts of the world.", "Adding a snack or dessert option to meal kits would be interesting."]
    }
    
    if entry_id in preferred_answers:
        return random.choice(preferred_answers[entry_id])
    
    return random.choice(options) if options else "Random response"

def generate_request_body(url: str, only_required=False):
    ''' Generate random request body data '''
    data = form.get_form_submit_request(
        url,
        only_required=only_required,
        fill_algorithm=fill_random_value,
        output="return",
        with_comment=False
    )
    data = json.loads(data)
    return data

def submit(url: str, data: any):
    ''' Submit form to url with data at random intervals '''
    url = form.get_form_response_url(url)
    print("Submitting to", url)
    print("Data:", data, flush=True)
   
    time.sleep(random.uniform(0.5, 2.0))  # Faster random delay before submission
    res = requests.post(url, data=data, timeout=5)
    if res.status_code != 200:
        print("Error! Can't submit form", res.status_code)

def main(url, only_required=False):
    try:
        for _ in range(20):  # Submit 20 responses
            payload = generate_request_body(url, only_required=only_required)
            submit(url, payload)
            print("Response submitted!")
            time.sleep(random.uniform(3, 10))  # Faster random delay between submissions
        print("Done!!!")
    except Exception as e:
        print("Error!", e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Submit Google Form with custom data')
    parser.add_argument('url', help='Google Form URL')
    parser.add_argument('-r', '--required', action='store_true', help='Only include required fields')
    args = parser.parse_args()
    main(args.url, args.required)
