from canvasapi import Canvas as cv
import json
import datetime
import requests

class Canvas:
    def __init__(self, api_token, url, active_courses):
        self.api_token = api_token
        self.url = url
        self.today = datetime.date.today()
        self.active_courses = active_courses
        self.canvas = cv(self.url, self.api_token)

    def getCourses(self):
        courses = self.canvas.get_courses(enrollment_type='student', enrollment_status='active')
        my_courses = []
        j = 0
        # use active_courses to get the active course objects
        for i in self.active_courses:
            for course in courses:
                try:
                    if (i == course.course_code):
                        j = course
                except:
                    continue
            my_courses.append(j)
            j = 0
        return my_courses

    def getAsssignments(self):
        my_courses = self.getCourses()
        # get assignments
        assignments = []
        for i in my_courses:
            assignments.append(i.get_assignments())
            # print(i.get_assignments()[0])

        # fix due dates
        for a in range(len(assignments)):
            for obj in assignments[a]:
                try:
                    # Example input date string
                    date_string = obj.due_at

                    # Convert string to datetime object
                    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")

                    # Subtract 4 hours from datetime object
                    new_date_object = date_object - datetime.timedelta(hours=4)

                    # Convert datetime object back to string in the original format
                    new_date_string = new_date_object.strftime("%Y-%m-%dT%H:%M:%SZ")

                    obj.due_at = new_date_string
                except:
                    continue

        dates = []
        upcoming_assignments = []
        classes_list = []

        for a in range(len(assignments)):
            for obj in assignments[a]:
                try:
                    obj_date = datetime.datetime.strptime(obj.due_at, "%Y-%m-%dT%H:%M:%SZ")
                    if (obj_date.date() >= self.today):
                        dates.append(obj_date)
                        classes_list.append(a)
                        upcoming_assignments.append(obj)
                except:
                    continue
                # print(obj.due_at, end='')
                # print(my_courses[a].course_code)
        # handle assignments
        assignments_data = {}
        for num in range(len(upcoming_assignments)):
            assignments_data[f"Assignment_{num}"] = {
                "name": upcoming_assignments[num].name,
                "due_date": str((datetime.datetime.strptime(upcoming_assignments[num].due_at,
                                                            "%Y-%m-%dT%H:%M:%SZ")).date().strftime('%A %b %d')),
                "due_date_for_computer": upcoming_assignments[num].due_at,
                "class": my_courses[classes_list[num]].course_code
            }
        # print(json.dumps(assignments_data))

        # Return only assignments due within the next week
        target_date = self.today + datetime.timedelta(days=7)
        display_assignments = []
        for assign in assignments_data:
            obj_date = datetime.datetime.strptime(assignments_data[assign]["due_date_for_computer"],
                                                  "%Y-%m-%dT%H:%M:%SZ")
            if (obj_date.date() <= target_date and obj_date.date() >= self.today):
                display_assignments.append(assignments_data[assign])

        return_assignment_portion = {}
        for num in range(len(display_assignments)):
            return_assignment_portion[f"Assignment_{num}"] = display_assignments[num]

        sorted_assignments = dict(sorted(return_assignment_portion.items(), key=lambda x: x[1]["due_date_for_computer"], reverse=True))
        i = 0
        final_return = {}
        for assign in sorted_assignments:
            # print(assign)
            final_return[f'Assignment_{i}'] = sorted_assignments[assign]
            i = i + 1

        return(final_return)

    def getAnnouncements(self):
        my_courses = self.getCourses()
        # Set the headers with the access token
        headers = {
            'Authorization': 'Bearer ' + self.api_token,
        }
        # Make the GET request to the API
        select_announcements = []
        target_date = self.today - datetime.timedelta(days=7)
        all_announcements = []
        for course in my_courses:
            response = requests.get(self.url + f'api/v1/announcements?context_codes[]=course_{course.id}',
                                    headers=headers).json()
            all_announcements.append(response)
        for course in all_announcements:
            for announcement in course:
                obj_date = datetime.datetime.strptime(announcement["last_reply_at"], "%Y-%m-%dT%H:%M:%SZ")
                if (obj_date.date() >= target_date):
                    select_announcements.append(announcement)
        display_announcements = []
        for announcement in select_announcements:
            announcement_obj = {
                'id': announcement['id'],
                'title': announcement['title'],
                'date': str(
                    (datetime.datetime.strptime(announcement['last_reply_at'], "%Y-%m-%dT%H:%M:%SZ")).date().strftime(
                        '%A %b %d')),
                'course': announcement['context_code']
            }
            display_announcements.append(announcement_obj)

        return display_announcements