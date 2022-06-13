    if convert['children']:
			for child in convert['children']:
				child_id=self.get_map_field_by_src(self.TYPE_CHILD, child['id'], child['code'])
				if child_id:
					self.log(child_id,"child_id")
					var_post_data={
							"variant": {
								'price': child['price'],
						}
					}
					var_response = self.api('variants/' + to_str(child_id) + '.json', var_post_data, 'Put')
					var_response = json_decode(var_response)
		else:
			product_id=self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
			if product_id:
				get_response = self.api('products/' + to_str(product_id) + '.json', api_type='get')
				get_response = json_decode(get_response)
				variant_id=get_response['product']['variants'][0]['id']
				var_post_data={
							"variant": {
								'price': to_str(round(to_decimal(convert['price']), 2)) if to_decimal(convert['price']) > 0 else 0,
						}
					}
				response = self.api('variants/' + to_str(variant_id) + '.json', var_post_data, 'Put')
				response = json_decode(response)	
