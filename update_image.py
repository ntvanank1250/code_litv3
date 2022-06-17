description, tag
		self.log(convert, "convert_log")
		product_name = product['title']
		r = self.select_raw("select * from product_check where product_name = '" + product_name+"'")
		r = r['data']
		# tags = convert['tags']
		# add tag and des
		if r:
			self.log(r, "query_log")
			for row in r:
				id_desc = to_str(row["product_id"])
				id_variant=to_str(row['id'])
				q=self.query_raw("UPDATE product_check SET `product_desc` = '" + id_desc+ "' WHERE `product_id` = '" + id_desc +"'and `id` = '"+ id_variant+"'")
			put_data = {
						'product': {
							'id': id_desc,
							'body_html': to_str(convert['description']),
							'tags': tags,
							'images': list()
					}
				}
			response = self.api('products/' + to_str(id_desc) + '.json', put_data, 'PUT')
			response = json_decode(response)
			self.log(response, "response_log1")
			
			# image
			images = list()
			

			if convert['thumb_image']['url']:
				image_thumb= {'image':{
								'src': convert['thumb_image']['url']
								}
							}
				response = self.api('products/' + to_str(id_desc) + '/images.json', image_thumb, 'POST')
				response = json_decode(response)
				self.insert_map('img_shopify',None,response['image']['id'],convert['thumb_image']['url'])
				self.log(images,'images_log')	
			if convert['images']:
				for image_convert in convert['images']:
					if image_convert['url']:
						image= {'image':{
								'src': image_convert['url']
							}
						}
						response = self.api('products/' + to_str(id_desc) + '/images.json', image, 'POST')
						response = json_decode(response)
						self.insert_map('img_shopify',None,response['image']['id'],image_convert['url'])
						self.log(images,'images_log')

			

			### update image for chirdren
			option_list_desc=list()

			for row in r:
				id_and_option={
					'id':row['id'],
					'option':set(row['option'].split(';'))
				}
				option_list_desc.append(id_and_option)

			for child in convert['children']:
				option_src=list()
				for child_att in child['attributes']:
					option_src.append(child_att['option_value_name'])
				option_src=set(option_src)
				self.log(option_src,"option_src")
				id__variant_desc=None
				for i in option_list_desc:
					if option_src==i['option']:
						id__variant_desc=i['id']
						self.log(id__variant_desc,"id__variant_desc")
						break
				if id__variant_desc:
					image_id = self.get_map_field_by_src('img_shopify',None,child['thumb_image']['url'])
					
					put_variant={
						'variant':{
							'image_id':image_id
						}
					}
					response = self.api('variants/' + to_str(id__variant_desc) + '.json', put_variant, 'PUT')
					response = json_decode(response)
