---
title: "Some checklist workflows for working with REST APIs"
subtitle: "INST447, Spring 2026"
author: "Scott Jackson"
---

# Big Picture

1. Read the documentation
2. Figure out authentication
  - Open?
  - Key?
  - OAuth?
  - other?
3. Is there an existing Python library?
4. Is it REST, or something else?
  - And do you know how to access?
5. What are the rules you need to follow?
  - Rate?
  - Request limits?
6. Make an example request
7. Explore your example data
8. Structure your code
  - Make it reproducible!

# Approaching the code

1. Slice and dice the example data
  - type()
  - len()
  - dict.keys()
2. Figure out what you want
3. Structure your dictionary to be populated
4. Write your code to populate your dictionary
5. Convert dictionary to pandas.DataFrame or other convenient object
