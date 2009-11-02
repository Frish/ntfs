DELIMS = " \\t\\r\\n"   -- delimiters of tokenizing
OPTFREQ = 0.1        -- frequency of optimization
LIMNUM = 500         -- limit number of kept occurrence

function _tokenize(text, delims)
   local tokens = {}
   for token in string.gmatch(text, "[^" .. delims .. "]+") do
      if #token > 0 then
         table.insert(tokens, token)
      end
   end
   return tokens
end

function put(id, text)
   id = tonumber(id)
   if not id or id < 1 then
      return nil
   end
   if not text then
      return nil
   end
   local opt = math.random() < OPTFREQ
   local tokens = _tokenize(text, DELIMS)
   local idsel = _pack("w", id)
   for i = 1, #tokens do
      token = tokens[i]
      if not _lock(token) then
         break
      end
      if opt then
         local ids = {}
         local idsel = _get(token)
         if idsel then
            ids = _unpack("w*", idsel)
         end
         local nids = {}
         local top = #ids - LIMNUM + 2
         if top < 1 then
            top = 1
         end
         for j = top, #ids do
            table.insert(nids, ids[j])
         end
         table.insert(nids, id)
         idsel = _pack("w*", nids)
         _put(token, idsel)
      else
         _putcat(token, idsel)
      end
      _unlock(token)
   end
   return "ok"
end

DEFMAX = 10          -- default maximum number of search

function search(phrase, max)
   if not phrase then
      return nil
   end
   max = tonumber(max)
   if not max or max < 0 then
      max = DEFMAX
   end
   local tokens = _tokenize(phrase, DELIMS)
   local hits = {}
   local tnum = #tokens
   for i = 1, tnum do
      local idsel = _get(tokens[i])
      if idsel then
         local ids = _unpack("w*", idsel)
         local uniq = {}
         for j = 1, #ids do
            local id = ids[j]
            if not uniq[id] then
               local old = hits[id]
               if old then
                  hits[id] = old + 1
               else
                  hits[id] = 1
               end
               uniq[id] = true
            end
         end
      end
   end
   local result = {}
   for id, num in pairs(hits) do
      if num == tnum then
         table.insert(result, id)
      end
   end
   table.sort(result)
   local rtxt = #result .. "\\n"
   local bot = #result - max
   if bot < 1 then
      bot = 1
   end
   for i = #result, bot, -1 do
      if max < 1 then
         break
      end
      rtxt = rtxt .. result[i] .. "\\n"
      max = max - 1
   end
   return rtxt
end

