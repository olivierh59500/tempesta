#!/usr/bin/env python

# #659 A functional test of schedulers of the Tempesta.

import apache
import conf
class Test:
	vh_curr = 1
	sg_curr = 1
	def __init__(self):
		self.cfg = conf.TFWConfig()
		self.apache_cfg = conf.ApacheConfig()
		self.cfg.add_option('listen', '8081')

	def add_sg(self, h_num, sched='round-robin'):
		self.cfg.add_string("")
		self.cfg.add_section('srv_group '  + 'group' +
				     str(self.sg_curr) + ' sched=' + sched)
		for x in range(0, h_num):
			h_name = 'sched_' + str(self.vh_curr) + '.org'
			port = self.apache_cfg.add_vhost(h_name)
			self.cfg.add_option('server', '127.0.0.1:' + str(port))
			self.vh_curr += 1
		self.cfg.add_end_of_section()
		self.cfg.add_string("")
		
		self.sg_curr += 1

	def add_rules(self,host='sched'):
		self.cfg.add_string("")
		self.cfg.add_section('sched_http_rules')
		for x in range(1, self.sg_curr):
			self.cfg.add_option('match ' + 'group' + 
					    str(x),' host eq '+
					    host + str(x))
		self.cfg.add_end_of_section()
		
	
	def run(self):
		for x in range(1, 25):
			self.add_sg(x)
		for x in range(1, 25):
			self.add_sg(x)
		for x in range(1, 25):
			self.add_sg(x)
#		self.add_sg(5, sched='round-robin')
#		self.add_sg(5, sched='hash')
		self.add_rules('sched')
#		capache = conf.ApacheConfig()
#		capache.add_vhost('sched2.org')
	
	def get_name(self):
		return 'test schedulers'
