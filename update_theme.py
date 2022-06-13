product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
	if product_id:
		# upload file and add to metafield
		if "files" in convert and convert['files']:
			theme_id = 132918018298		
			for file in convert['files']:
				file_code = self.get_map_field_by_src('pdf', file['id'], file['url'], field= 'code_desc')
				if not file_code:
					asset_put_file_data = {
						"asset": {
							"key": "assets/{}".format(file['handle']),
							"theme_id": theme_id,
							"src": file['url']
						}
					}
					upload_file_res = self.api(f"themes/{theme_id}/assets.json", asset_put_file_data, "PUT")
					self.log(upload_file_res, '__upload_file_res')
					upload_file_data = dict(json_decode(upload_file_res))
					if "asset" in upload_file_data and upload_file_data["asset"]:
						self.log(upload_file_data, '__upload_file_data')
						self.insert_map('pdf', id_src= file['id'], code_src= file['url'], code_desc= upload_file_data["asset"]['public_url'])

			if len(convert['files']) <= 1:
				for file in convert['files']:
					file_code = self.get_map_field_by_src('pdf', file['id'], file['url'], field= 'code_desc')
					self.log(file_code,'__file_code')
					if file_code:
						meta_file_post_data = {
							"metafield": {
								"key": "PDF",
								"value": file_code,
								"namespace": "global",
								"owner_id": product_id,
								"type": "url"
							}
						}
						file_res = self.api("products/{}/metafields.json".format(product_id), meta_file_post_data, "POST")
						self.log(file_res,'__file_res')
			elif len(convert['files']) > 1:
				for i, file in enumerate(convert['files']):
					file_code = self.get_map_field_by_src('pdf', file['id'], file['url'], field= 'code_desc')
					self.log(file_code,'__file_code')
					if file_code:
						meta_file_post_data = {
							"metafield": {
								"key": f"PDF_{i}",
								"value": file_code,
								"namespace": "global",
								"owner_id": product_id,
								"type": "url"
							}
						}
						file_res = self.api("products/{}/metafields.json".format(product_id), meta_file_post_data, "POST")
						self.log(file_res,'__file_res')
