## xóa từng cái một trên target và trên map. lần nào chạy xóa lần đó
order_id = self.get_map_field_by_src(self.TYPE_ORDER, convert['id'], convert['code'])
if order_id:
	self.api('orders/'+to_str(order_id)+'.json',None,'DELETE')
	self.select_raw("DELETE FROM migration_map WHERE type = 'order' AND id_src = "+to_str(convert['id']))
	
	
if id_desc:
	self.api('products/'+to_str(id_desc)+'.json',None,'DELETE')
	self.select_raw("DELETE FROM migration_map WHERE type = 'product' AND id_src = "+to_str(convert['id']))
	for child in convert['children']:
		self.select_raw("DELETE FROM migration_map WHERE type = 'product_child' AND id_src = "+to_str(child['id']))

  
 ## xóa hết 1 lần tùy entity mà phần xóa map thay đổi

 if 'product' not in self._notice:
	self._notice['product'] = True
	self.clear_target_products()
	self.delete_obj('migration_map', where={'migration_id': self._migration_id, 'type': 'product'})
	self.delete_obj('migration_map', where={'migration_id': self._migration_id, 'type': 'product_child'})
	self.delete_obj('migration_map', where={'migration_id': self._migration_id, 'type': 'attr'})
	self.delete_obj('migration_map', where={'migration_id': self._migration_id, 'type': 'attr_option'})
	self.delete_obj('migration_map', where={'migration_id': self._migration_id, 'type': 'attr_value'})
