    id_desc= self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
		s=self.select_raw("select * from migration_map where id_desc = '" + to_str(id_desc) + "'")
		self.log(id_desc, 'id_desc')
		s_data=s['data'][0]
		self.log(s_data, 's_data')
		detail=s_data['code_desc']
		new_meta={"metafield":{
						"value":detail,
						"namespace": "my_fields", 
						"key": "detail",
			}}
		response = self.api('products/'+ to_str(id_desc) + '/metafields.json', new_meta, api_type='post')
		response = json_decode(response)
		self.log(response,'response')
