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


def wrap_func(results, limit, offset, total):
    header = dict()
    header["count"] = len(results)
    header["limit"], header["offset"] = limit, offset
    header["total"] = total
    return {"metadata": {"result_set": header}, "results": results}


def wrap_link(href: str, rel: str):
    link = dict()
    link["href"] = href
    link["rel"] = rel
    return link
