function max(s,e)
    -- ex: mapreducetest_hello_1247630400 86400
    local keys,j = {},1
    ks = _split(s,"_")
    f,db,t = ks[1],ks[2],ks[3]
    etime = t+e
    for i=t,etime,5*60 do
        s_key = os.date("%Y-%m-%d%%20%H%%3A%M%%3A%S",i)
        key = f.."_"..db.."_"..s_key
        keys[j] = key
        j=j+1
    end

    local res = 0
    function mapper(key, value, mapemit)
        if tonumber(value)>tonumber(res) then
            res = value
        end
        return true
    end
    
    function reducer(key, values)
        -- res = res .. key .. "\t" .. #values .. "\n"
        return true
    end
    
    if not _mapreduce(mapper, reducer,keys) then
        res = nil
    end
    return res
end