import os
import unittest
import tempfile

from backend.app import create_app


app = create_app()


class CategoryTestCase(unittest.TestCase):
    URL = '/api/categories/'

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_create(self):
        name = 'cat1'
        request = self.app.post(
            self.URL,
            json={'name': name},

        )

        json_data = request.get_json()
        assert 'id' in json_data
        assert name, json_data['name']

    def test_get_list(self):
        name = 'cat2'
        self.app.post(
            self.URL,
            json={'name': name},
        )
        request = self.app.get(
            self.URL
        )
        json_data = request.get_json()
        assert 0 < len(json_data)
        assert name == json_data[-1]['name']

    def test_get_object(self):
        name = 'cat3'
        request = self.app.post(
            self.URL,
            json={'name': name},

        )
        json_data = request.get_json()
        id = json_data['id']
        name = json_data['name']

        request = self.app.get(
            f'{self.URL}{id}'
        )

        json_data = request.get_json()
        assert 'id' in json_data
        assert name == json_data['name']

    def test_update_object(self):
        name = 'cat4'
        new_name = 'cat4_new'
        request = self.app.post(
            self.URL,
            json={'name': name},

        )
        json_data = request.get_json()
        id = json_data['id']
        name = json_data['name']

        request = self.app.put(
            f'{self.URL}{id}',
            json={'name': new_name},
        )

        json_data = request.get_json()
        assert 'id' in json_data
        assert new_name == json_data['name']

    def test_delete_object(self):
        name = 'cat5'
        request = self.app.post(
            self.URL,
            json={'name': name},

        )
        json_data = request.get_json()
        id = json_data['id']

        request = self.app.delete(
            f'{self.URL}{id}'
        )
        assert request.status, 200
        request = self.app.get(
            f'{self.URL}{id}'
        )
        assert request.status, 404


class TypeTestCase(unittest.TestCase):
    URL = '/api/types/'

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_create(self):
        name = 'type1'
        request = self.app.post(
            self.URL,
            json={'name': name},

        )

        json_data = request.get_json()
        assert 'id' in json_data
        assert name, json_data['name']

    def test_get_list(self):
        name = 'type2'
        self.app.post(
            self.URL,
            json={'name': name},
        )
        request = self.app.get(
            self.URL
        )
        json_data = request.get_json()
        assert 0 < len(json_data)
        assert name == json_data[-1]['name']

    def test_get_object(self):
        name = 'type3'
        request = self.app.post(
            self.URL,
            json={'name': name},

        )
        json_data = request.get_json()
        id = json_data['id']
        name = json_data['name']

        request = self.app.get(
            f'{self.URL}{id}'
        )

        json_data = request.get_json()
        assert 'id' in json_data
        assert name == json_data['name']

    def test_update_object(self):
        name = 'type4'
        new_name = 'type4_new'
        request = self.app.post(
            self.URL,
            json={'name': name},

        )
        json_data = request.get_json()
        id = json_data['id']
        name = json_data['name']

        request = self.app.put(
            f'{self.URL}{id}',
            json={'name': new_name},
        )

        json_data = request.get_json()
        assert 'id' in json_data
        assert new_name == json_data['name']

    def test_delete_object(self):
        name = 'type5'
        request = self.app.post(
            self.URL,
            json={'name': name},

        )
        json_data = request.get_json()
        id = json_data['id']

        request = self.app.delete(
            f'{self.URL}{id}'
        )
        assert request.status, 200
        request = self.app.get(
            f'{self.URL}{id}'
        )
        assert request.status, 404


class ProductTestCase(unittest.TestCase):
    URL = '/api/products/'

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_create(self):
        request = self.app.post(
            '/api/categories/',
            json={'name': 'product_category1'},

        )
        json_data = request.get_json()
        category_id = json_data['id']
        request = self.app.post(
            '/api/types/',
            json={'name': 'product_type1'},

        )
        json_data = request.get_json()
        type_id = json_data['id']

        json = {
            'name': 'product_name1',
            'sku': 'sku1',
            'stocks': 0,
            'category_id': category_id,
            'type_id': type_id,
        }
        request = self.app.post(
            self.URL,
            json=json,

        )
        json_data = request.get_json()
        assert 'id' in json_data
        assert json['name'], json_data['name']
        assert json['category_id'], json_data['category_id']
        assert json['type_id'], json_data['type_id']

    def test_get_list(self):
        request = self.app.post(
            '/api/categories/',
            json={'name': 'product_category2'},

        )
        json_data = request.get_json()
        category_id = json_data['id']
        request = self.app.post(
            '/api/types/',
            json={'name': 'product_type2'},

        )
        json_data = request.get_json()
        type_id = json_data['id']

        json = {
            'name': 'product_name2',
            'sku': 'sku2',
            'stocks': 0,
            'category_id': category_id,
            'type_id': type_id,
        }
        self.app.post(
            self.URL,
            json=json,

        )
        request = self.app.get(
            self.URL
        )
        json_data = request.get_json()
        assert 0 < len(json_data)
        assert json['name'] == json_data[-1]['name']

    def test_get_object(self):
        request = self.app.post(
            '/api/categories/',
            json={'name': 'product_category3'},

        )
        json_data = request.get_json()
        category_id = json_data['id']
        request = self.app.post(
            '/api/types/',
            json={'name': 'product_type3'},

        )
        json_data = request.get_json()
        type_id = json_data['id']

        json = {
            'name': 'product_name3',
            'sku': 'sku3',
            'stocks': 0,
            'category_id': category_id,
            'type_id': type_id,
        }
        request = self.app.post(
            self.URL,
            json=json,

        )
        json_data = request.get_json()
        id = json_data['id']
        name = json_data['name']

        request = self.app.get(
            f'{self.URL}{id}'
        )

        json_data = request.get_json()
        assert 'id' in json_data
        assert name == json_data['name']

    def test_update_object(self):
        request = self.app.post(
            '/api/categories/',
            json={'name': 'product_category4'},

        )
        json_data = request.get_json()
        category_id = json_data['id']
        request = self.app.post(
            '/api/types/',
            json={'name': 'product_type4'},

        )
        json_data = request.get_json()
        type_id = json_data['id']

        json = {
            'name': 'product_name4',
            'sku': 'sku4',
            'stocks': 0,
            'category_id': category_id,
            'type_id': type_id,
        }
        new_json = {
            'name': 'new_product_name4',
            'sku': 'new_sku4',
            'stocks': 5,
            'category_id': category_id,
            'type_id': type_id,
        }
        request = self.app.post(
            self.URL,
            json=json,

        )
        id = request.get_json()['id']
        request = self.app.put(
            f'{self.URL}{id}',
            json=new_json,
        )

        json_data = request.get_json()
        assert 'id' in json_data
        for key in new_json:
            assert new_json[key] == json_data[key]

    def test_delete_object(self):
        request = self.app.post(
            '/api/categories/',
            json={'name': 'product_category5'},

        )
        json_data = request.get_json()
        category_id = json_data['id']
        request = self.app.post(
            '/api/types/',
            json={'name': 'product_type5'},

        )
        json_data = request.get_json()
        type_id = json_data['id']

        json = {
            'name': 'product_name5',
            'sku': 'sku5',
            'stocks': 0,
            'category_id': category_id,
            'type_id': type_id,
        }
        request = self.app.post(
            self.URL,
            json=json,

        )
        json_data = request.get_json()
        id = json_data['id']

        request = self.app.delete(
            f'{self.URL}{id}'
        )
        assert request.status, 200
        request = self.app.get(
            f'{self.URL}{id}'
        )
        assert request.status, 404

    def test_reserve_object(self):
        request = self.app.post(
            '/api/categories/',
            json={'name': 'product_category_res'},

        )
        json_data = request.get_json()
        category_id = json_data['id']
        request = self.app.post(
            '/api/types/',
            json={'name': 'product_type_res'},

        )
        json_data = request.get_json()
        type_id = json_data['id']

        json = {
            'name': 'product_name_res',
            'sku': 'sku_res',
            'stocks': 10,
            'category_id': category_id,
            'type_id': type_id,
        }
        request = self.app.post(
            self.URL,
            json=json,

        )
        json_data = request.get_json()
        id = json_data['id']
        request = self.app.put(
            f'{self.URL}{id}/reserve-product',
            json={
                'stock_reserve': 4
            },
        )
        assert request.status, 200
        request = self.app.put(
            f'{self.URL}{id}/reserve-product',
            json={
                'stock_reserve': 50
            },
        )
        assert request.status, 400

    def test_bulk_edit(self):
        bulk_stocks = 50

        request = self.app.post(
            '/api/categories/',
            json={'name': 'product_category_bulk_edit'},

        )
        json_data = request.get_json()
        category_id = json_data['id']
        request = self.app.post(
            '/api/types/',
            json={'name': 'product_type_bulk_edit'},

        )
        json_data = request.get_json()
        type_id = json_data['id']

        ids = []
        for i in range(5):
            json = {
                'name': f'product_name_bulk_edit{i}',
                'sku': f'sku_bulk_edit{i}',
                'stocks': i,
                'category_id': category_id,
                'type_id': type_id,
            }
            request = self.app.post(
                self.URL,
                json=json,

            )
            json_data = request.get_json()
            ids.append(json_data['id'])
        request = self.app.put(
            f'{self.URL}/bulk-edit',
            json={
                'ids': ids,
                'fields': {
                    'stocks': 66
                }
            },
        )
        assert request.status, 200
        for id in ids:
            request = self.app.get(
                f'{self.URL}{id}'
            )
            json_data = request.get_json()
            assert bulk_stocks, json_data['stocks']


if __name__ == '__main__':
    unittest.main()
