import itertools
class TreeNode:
    def __init__(self,value,count,parent):
        self.value = value
        self.count = count
        self.parent = parent
        self.nodelink = None
        self.children = {}


def init_data(data):
    _data = {}
    for v in data:
        vv = frozenset(v)
        _data[vv] = _data.get(vv,0)+1
    return _data


def create_tree(data,support):
    _header = {}
    for v in data:
        for vv in v:
            _header[vv] = _header.get(vv,0)+data[v]
    header = {}
    for v in _header:
        if _header[v] >= support: header[v] = [_header[v],None]
    if len(header) == 0: return None

    node = TreeNode(None,None,None)
    for v in data:
        x = {}
        for vv in v:
            if vv in header: x[vv] = header[vv][0]
        if len(x) > 0:
            x = [r[0] for r in sorted(x.items(),key=lambda r:r[1],reverse=True)]
            update_tree(x,header,node,data[v])
    return header


def update_tree(x,header,node,count):
    if x[0] in node.children:
        node.children[x[0]].count += count
    else:
        node.children[x[0]] = TreeNode(x[0],count,node)
        if header[x[0]][1] is None:
            header[x[0]][1] = node.children[x[0]]
        else:
            _node = header[x[0]][1]
            while _node.nodelink is not None: _node = _node.nodelink
            _node.nodelink = node.children[x[0]]
    if len(x) > 1: update_tree(x[1:],header,node.children[x[0]],count)


def ascend_path(node):
    path = []
    while node.parent.value is not None:
        path.append(node.parent.value)
        node = node.parent
    return path


def find_prefix_path(node):
    data = {}
    while node is not None:
        path = ascend_path(node)
        if len(path) > 0: data[frozenset(path)] = node.count
        node = node.nodelink
    return data


def minetree(header,s,f,support):
    x = [r[0] for r in sorted(header.items(),key=lambda r:r[1][0])]
    for i in x:
        ss = s.copy()
        ss.add(i)
        f[tuple(ss)] = header[i][0]
        data = find_prefix_path(header[i][1])
        if len(data) > 0:
            new_header = create_tree(data,support)
            if new_header is not None:
                minetree(new_header,ss,f,support)


def subset(x):
    return itertools.chain(*[itertools.combinations(x,i+1) for i,a in enumerate(x)])


def get_confidence(f,confidence):
    confidence_data = {}
    for k in f:
        if len(k) > 1:
            kk = list(k)
            ss = subset(kk)
            kk = set(kk)
            for sv in ss:
                sv = set(sv)
                sd = tuple(kk.difference(sv))
                if len(sd) > 0:
                    sv = tuple(sv)
                    if sv in f:
                        cd = f[k]/f[sv]
                        if cd >= confidence: confidence_data[tuple([sv,sd])] = cd
    return confidence_data


if __name__ == '__main__':
    data = [[1, 2, 5], [2, 4], [2, 3], [1, 2, 4], [1, 3], [2, 3], [1, 3], [1, 2, 3, 5], [1, 2, 3]]
    data = init_data(data)
    header = create_tree(data, 2)
    support_data = {}
    minetree(header, set([]), support_data, 2)
    confidence_data = get_confidence(support_data, .6)
    print(support_data)
    print(confidence_data)