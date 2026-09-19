def detect_loop(mapping:dict[str,str]) -> list[list[str]]:
    loops=[]
    for start in mapping:
        seen=[]; cur=start
        while cur in mapping:
            if cur in seen:
                i=seen.index(cur); loops.append(seen[i:]+[cur]); break
            seen.append(cur); cur=mapping[cur]
    unique=[]
    for loop in loops:
        if loop not in unique: unique.append(loop)
    return unique

if __name__=="__main__":
    import json,sys
    mapping=json.load(open(sys.argv[1],encoding="utf-8"))
    loops=detect_loop(mapping)
    print(json.dumps({"pass":not loops,"loops":loops},indent=2))
    raise SystemExit(1 if loops else 0)
