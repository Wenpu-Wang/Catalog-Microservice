"""
{
   "metadata": {
      "result_set": {
         "count": 25,
         "offset": 0,
         "limit": 25,
         "total": 77
      },
      ...
"""


def wrap_func(res, limit, offset, total):
    header = dict()
    header["count"] = len(res)
    header["limit"], header["offset"] = limit, offset
    header["total"] = total
    return {"metadata": {"result_set": header}, "results": res}
