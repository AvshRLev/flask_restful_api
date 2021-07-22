import unittest
import requests
import main
import sqlite3

def get_number_of_dv_rows():
    connection_obj = sqlite3.connect('database.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("SELECT * FROM video_model")
    db_rows = (len(cursor_obj.fetchall()))
    connection_obj.close()
    return db_rows

BASE = "http://127.0.0.1:5000/"
data = [
    {"likes": 10, "name": "a clip", "views": 10000},
    {"likes": 11, "name": "a film", "views": 10001},
    {"likes": 12, "name": "a movie", "views": 10002}
]

class TestAPI(unittest.TestCase):
    def setUp(self):        
        for i in range(len(data)):
            requests.put(BASE + f"video/{str(i)}", data[i])  
    
    def tearDown(self):
        for i in range(get_number_of_dv_rows()):
            requests.delete(BASE + f"video/{str(i)}")  

    def test_get_video(self):
        response = requests.get(BASE + "video/0")
        self.assertEqual(response.json(), {"id": 0, "likes": 10, "name": "a clip", "views": 10000})

    def test_get_video_at_nonexisting_index(self):
        response = requests.get(BASE + "video/10")
        self.assertEqual(response.json(), {'message': 'Could not find video with this ID'})

    def test_get_all_videos(self):
        all_vids = requests.get(BASE + "videos")
        self.assertEqual(all_vids.json(), [{'id': 0, 'name': 'a clip', 'views': 10000, 'likes': 10}, {'id': 1, 'name': 'a film', 'views': 10001, 'likes': 11}, {'id': 2, 'name': 'a movie', 'views': 10002, 'likes': 12}])

    def test_add_video_to_db(self):
        response = requests.put(BASE + "video/3", {'name': 'a short film', 'views': 10003, 'likes': 13})
        self.assertEqual(response.json(), {'id': 3, 'name': 'a short film', 'views': 10003, 'likes': 13})
        
    def test_add_video_at_existing_index(self):    
        response = requests.put(BASE + "video/1", {'name': 'a short film', 'views': 10003, 'likes': 13})
        self.assertEqual(response.json(), {'message': 'Video ID Taken'})
        
    def test_add_video_with_invalid_data(self):
        response = requests.put(BASE + "video/1", {'name': 'a short film', 'v': 10003, 1: 13})
        self.assertEqual(response.json(), {'message': {'views': 'Views of The Video is required'}})

        response = requests.put(BASE + "video/1", {'name': 'a short film', 'views': 10003, 1: 13})
        self.assertEqual(response.json(), {'message': {'likes': 'Likes on The Video is required'}})

        response = requests.put(BASE + "video/1", {'n': 'a short film', 'views': 10003, "likes": 13})
        self.assertEqual(response.json(), {'message': {'name': 'Name of The Video is required'}})

        with self.assertRaises(TypeError):
            requests.put(BASE + "video/1", {'n': 'a short film', 'views': 10003, [1, 2]: 13})
        

    def test_update_video_details(self):
        response = requests.patch(BASE + "video/2", {"views": 10, "likes": 9})
        self.assertEqual(response.json(), {'id': 2, 'name': 'a movie', 'views': 10, 'likes': 9})

    def test_update_video_at_nonexisting_index(self):
        response = requests.patch(BASE + "video/10", {"views": 10, "likes": 9})
        self.assertEqual(response.json(), {'message': 'Could not find video with this ID'})

    def test_update_video_with_invalid_data(self):
        response = requests.patch(BASE + "video/0", {"chickens": 10, 5 : 9})
        self.assertEqual(response.json(), {'id': 0, 'likes': 10, 'name': 'a clip', 'views': 10000})

        with self.assertRaises(TypeError):
            requests.patch(BASE + "video/0", {"chickens": 10, [5, 7] : 9})
    

    def test_delete_video(self):
        response = requests.delete(BASE + "video/0")
        self.assertEqual(response.json(), {'Video 0 Deleted successfully': 204})

    def test_delete_video_at_nonexisting_index(self):
        response = requests.delete(BASE + "video/10")
        self.assertEqual(response.json(), {'message': 'Could not find video with this ID'})

if __name__ == "__main__":
    unittest.main()