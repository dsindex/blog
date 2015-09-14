#!/usr/bin/env python
#-*- coding: utf8 -*-

import os
from optparse import OptionParser

# global variable
VERBOSE = 0

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# -------------------------------------------------------------------------
# build tree
# -------------------------------------------------------------------------
def next_paren(tokens, i) :
	'''
	tokens[i]에서 시작해서 다음 '(' 혹은 ')'의 위치를 탐색
	못찾은 경우 return -1 
	'''
	j = 0
	found = False
	for token in tokens[i:] :
		if token == '(' or token == ')' : 
			found = True
			break
		j += 1
	if found : return i + j
	return -1

def node_string(node, enable_eoj=True) :
	if node['leaf'] : 
		if enable_eoj :
			return '(' + node['label'] + ' ' + node['eoj'] + '/' + str(node['eoj_idx']) + ' ' + node['morphs'] + ')'
		else :
			return '(' + node['label'] + ' ' + node['morphs'] + ')'
	else :
		return '(' + node['label'] + ')'

def create_node(tokens, i, j) :
	'''
	i ~ j까지가 label,morphs 영역
	i + 1 = j  : label
	             ex) '( NP ('
				        i  j
	i + 1 < j  : label,morphs
	             ex) '( NP_MOD 프랑스/NNP+의/JKG )'
				        i                        j
	'''
	node = {'lchild':{}, 'rchild':{}, 'parent':{}, 'sibling':{}}
	if i + 1 == j :
		node['label'] = tokens[i]
		node['leaf']  = False
		return node
	elif i + 1 < j :
		node['label'] = tokens[i]
		node['morphs']  = tokens[i+1]
		node['leaf']  = True
		return node
	else :
		return None

def make_edge(top, node) :
	if not top['lchild'] : # link to left child
		top['lchild'] = node
		node['parent'] = top
		if VERBOSE : print node_string(top) + '-[left]->' + node_string(node)
	elif not top['rchild'] : # link to right child
		top['rchild'] = node
		node['parent'] = top
		top['lchild']['sibling'] = node
		if VERBOSE : print node_string(top) + '-[right]->' + node_string(node)
	else :
		return False
	return True	

def build_tree(sent, tokens) :
	'''
	sent = ; 프랑스의 세계적인 의상 디자이너 엠마누엘 웅가로가 실내 장식용 직물 디자이너로 나섰다.
	tokens = ( S ( NP_SBJ ( NP ( NP_MOD 프랑스/NNP+의/JKG ) \
			( NP ( VNP_MOD 세계/NNG+적/XSN+이/VCP+ᆫ/ETM ) ( NP ( NP 의상/NNG ) ( NP 디자이너/NNG ) ) ) ) \
			( NP_SBJ ( NP 엠마누엘/NNP ) ( NP_SBJ 웅가로/NNP+가/JKS ) ) ) \
			( VP ( NP_AJT ( NP ( NP ( NP 실내/NNG ) ( NP 장식/NNG+용/XSN ) ) ( NP 직물/NNG ) ) \
			( NP_AJT 디자이너/NNG+로/JKB ) ) ( VP 나서/VV+었/EP+다/EF+./SF ) ) )
	'''
	err = ' '.join(tokens)
	root = {'lchild':{}, 'rchild':{}, 'parent':{}, 'sibling':{}, 'leaf':False, 'label':'ROOT'}
	stack = []
	stack.append(root)
	max = len(tokens)
	i = 0
	eoj_idx = 1
	eoj_max = len(sent)
	while i < max :
		token = tokens[i]
		if token == '(' : # create node and push
			j = next_paren(tokens, i+1)
			if j == -1 or i+1 == j : 
				sys.stderr.write("ill-formed parentheses[1] : %s\n" % (err))
				return None
			node = create_node(tokens, i+1, j)
			if not node : return None
			# assign eoj/eoj_idx to leaf node
			if node['leaf'] :
				if eoj_idx >= eoj_max :
					sys.stderr.write("not aligned sentence %s : %s\n" % (' '.join(sent), err))
					return None
				node['eoj'] = sent[eoj_idx]
				node['eoj_idx'] = eoj_idx
				eoj_idx += 1
			if VERBOSE : print node_string(node)
			# push to stack
			stack.append(node)
		if token == ')' :
			# pop and make edge
			if len(stack) == 0 : 
				sys.stderr.write("ill-formed parentheses[2] : %s\n" % (err))
				return None
			node = stack.pop()
			if len(stack) == 0 : 
				sys.stderr.write("ill-formed parentheses[3] : %s\n" % (err))
				return None
			top  = stack[-1]
			if not make_edge(top, node) :
				sys.stderr.write("can't make edge : %s\n" % (err))
				return None
		i += 1

	if len(stack) == 1 and stack[-1]['label'] == 'ROOT' :
		return root
	else :
		sys.stderr.write("build failure : %s\n" % (err))
		return None
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# preprocessing
# -------------------------------------------------------------------------
def modify_illformed_1(tokens) :
	# ex) '( NP ( NP ( NP ( NP+포로/NNG )'
	# '(' 다음이 label인데 '+'가 포함되어 있으면 처음 '+'만 공백으로
	n_tokens = []
	max = len(tokens)
	i = 0
	while i < max :
		token = tokens[i]
		if token == '(' :
			n_tokens.append(token)
			if '+' in tokens[i+1] :
				t_list = tokens[i+1].split('+')
				n_tokens.append(t_list[0]) # label
				n_tokens.append(''.join(t_list[1:])) # morphs
				i += 1
		else :
			n_tokens.append(token)
		i += 1
	return n_tokens

def tokenize(bucket) :
	'''
	* 다루기 쉽도록 공백으로 분리된 token 단위로 변환한다. 
	예) bucket
	; 프랑스의 세계적인 의상 디자이너 엠마누엘 웅가로가 실내 장식용 직물 디자이너로 나섰다.
	(S	(NP_SBJ	(NP	(NP_MOD 프랑스/NNP + 의/JKG)
				(NP	(VNP_MOD 세계/NNG + 적/XSN + 이/VCP + ᆫ/ETM)
					(NP	(NP 의상/NNG)
						(NP 디자이너/NNG))))
			(NP_SBJ	(NP 엠마누엘/NNP)
				(NP_SBJ 웅가로/NNP + 가/JKS)))
		(VP	(NP_AJT	(NP	(NP	(NP 실내/NNG)
						(NP 장식/NNG + 용/XSN))
					(NP 직물/NNG))
				(NP_AJT 디자이너/NNG + 로/JKB))
			(VP 나서/VV + 었/EP + 다/EF + ./SF)))
	'''
	sent = bucket[0].split()
	if sent[0] != ';' : return None,None
	paren_parse = ' '.join([s.strip('\t').replace('\t',' ') for s in bucket[1:]])
	paren_parse = paren_parse.replace(' + ','+')
	paren_parse = paren_parse.replace('(/','^[/').replace(')/','^]/')
	paren_parse = paren_parse.replace('(',' ( ').replace(')',' ) ')
	paren_parse = paren_parse.replace('^[/','(/').replace('^]/',')/')
	paren_parse = paren_parse.replace('+ ','+')
	tokens = paren_parse.split()
	tokens = modify_illformed_1(tokens)

	if VERBOSE : print ' '.join(tokens)
	return sent, tokens
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# tree traversal
# -------------------------------------------------------------------------
def tree2tokens(node, tokens, depth=0) :
	'''
	입력을 tree로 변환하기 전 tokenizing 했는데,
	여기서는 tree를 가지고 역으로 tokenizing 결과를 만든다. 
	'''
	if node['leaf'] :
		tokens.append('(')
		tokens.append(node['label'])
		tokens.append(node['morphs'])
		tokens.append(')')
	else :
		tokens.append('(')
		tokens.append(node['label'])

	if node['lchild'] : 
		tree2tokens(node['lchild'], tokens, depth=depth+1)
		if not node['rchild'] :
			tokens.append(')') # closed
	if node['rchild'] : 
		tree2tokens(node['rchild'], tokens, depth=depth+1)
		tokens.append(')') # closed

def modify_morphs(morphs) :
	try : 
		t_morphs = morphs.replace('++/','+\t/') # + -> tab
		t_morphs = t_morphs.replace('+',' + ')
		t_morphs = t_morphs.replace('\t','+')   # tab -> +
	except :
		return morphs
	return t_morphs

def tree2con(node, tokens, history, depth=0) :
	'''
	입력을 tree로 변환했다면, 여기서 다시
	tree를 입력과 같은 형태(constituent, phrase structure)로 출력한다. 
	'''
	if depth == 0 : prev_node = None
	else : prev_node = history[-1]
	if prev_node and prev_node['leaf'] : # 바로 전에 leaf를 찍었다면
		tokens.append('\n')
		for i in xrange(depth) :
			tokens.append('\t')

	if node['leaf'] :
		tokens.append('(' + node['label'] + ' ' + modify_morphs(node['morphs']) + ')')
	else :
		tokens.append('(' + node['label'] + '\t')
	history.append(node)

	if node['lchild'] : 
		tree2con(node['lchild'], tokens, history, depth+1)
		if not node['rchild'] :
			tokens.append(')') # closed
	if node['rchild'] : 
		tree2con(node['rchild'], tokens, history, depth+1)
		tokens.append(')') # closed

def is_vx(morphs) :
	tokens = morphs.split('+')
	if '/VX' in tokens[0] : return True
	return False

def check_vx_rule(gov_node) :
	if not gov_node['parent'] : return False
	if not gov_node['parent']['lchild'] : return False
	# 태그가 'VX'로 시작
	if not is_vx(gov_node['morphs']) : return False
	return True

def find_gov(node) :
	'''
	* node = leaf node

	1. head final rule
	  - 현재 node에서 parent를 따라가면서
 	    첫번째로 right child가 있는 node를 만나면
	    해당 node의 right child를 따라서 leaf node까지 이동
	2. VX rule
	  - 보조용언을 governor로 갖는다면 본용언으로 바꿔준다. 
	'''
	# 첫번째로 right child가 있는 node를 탐색
	# sibling link를 활용한다. 
	next = node
	found = None
	while next :
		if next['sibling'] :
			found = next['sibling']['parent']
			break
		next = next['parent']

	gov_node = None
	if found :
		# right child를 따라서 leaf node까지
		next = found
		while next :
			if next['leaf'] :
				gov_node = next
				# -----------------------------------------------------------------
				# gov_node의 태그가 'VX'로 시작하는 경우 parent->lchild를 따라간다. 
				if check_vx_rule(gov_node) :
					t_next = gov_node['parent']
					while t_next :
						# 본용언이 보조용언을 governor로 갖는 경우는 예외
						if t_next['leaf'] and t_next['eoj_idx'] != node['eoj_idx'] :
							gov_node = t_next
							break
						t_next = t_next['lchild']
				# -----------------------------------------------------------------
				break
			next = next['rchild']
	if gov_node :
		return gov_node['eoj_idx']
	return 0
		

def tree2dep(node, depth=0) :
	'''
	tree에서 dependency 구조를 뽑아낸다. 
	'''
	if node['leaf'] :
		eoj_idx = node['eoj_idx']
		eoj     = node['eoj']
		morphs  = modify_morphs(node['morphs'])
		label   = node['label']
		gov     = find_gov(node)
		out = [eoj_idx, eoj, morphs, label, gov]
		print '\t'.join([str(e) for e in out])
	if node['lchild'] : 
		tree2dep(node['lchild'], depth+1)
	if node['rchild'] : 
		tree2dep(node['rchild'], depth+1)
# -------------------------------------------------------------------------

def spill(bucket, mode) :

	# --------------------------------------------------------------
	# ill-formed filtering and build tree
	sent, tokens = tokenize(bucket)
	if not sent : return False
	tree = build_tree(sent, tokens)
	if not tree : return False
	# begin with tree['lchild'](ROOT 제외)
	t_tokens = []
	tree2tokens(tree['lchild'], t_tokens, depth=0)
	if tokens != t_tokens :
		sys.stderr.write("input parentheses != tree2tokens\n")
		sys.stderr.write("input        = %s\n" % (' '.join(tokens)))
		sys.stderr.write("tree2tokens  = %s\n" % (' '.join(t_tokens)))
		return False
	# --------------------------------------------------------------

	if mode == 0 : # print constituent tree
		print ' '.join(sent)
		t_tokens = []
		history  = []
		tree2con(tree['lchild'], t_tokens, history, depth=0)
		print ''.join(t_tokens).strip()
		print '\n',
		return True
	if mode == 1 : # print dependency tree
		tree2dep(tree['lchild'], depth=0)
		print '\n',
		return True

if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("--verbose", action="store_const", const=1, dest="verbose", help="verbose mode")
	parser.add_option("-m", "--mode", dest="mode", help="mode : 0(constituent), 1(dependency)", metavar="mode")
	(options, args) = parser.parse_args()

	if options.verbose : VERBOSE = 1

	mode = options.mode
	if mode == None : mode = 0
	else : mode = int(mode)

	bucket = []
	while 1:
		try:
			line = sys.stdin.readline()
		except KeyboardInterrupt:
			break
		if not line:
			break
		line = line.strip()

		if not line and len(bucket) >= 1 : 
			ret = spill(bucket, mode)
			bucket = []
			continue

		bucket.append(line)

	if len(bucket) != 0 :
		ret = spill(bucket, mode)

