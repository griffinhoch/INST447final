# some common operations of combining and reshaping data

import pandas as pd
import time

# We want to combine information about average wages and populations for Maryland counties

# data from Maryland's Open Data portal
wages = pd.read_csv("/Users/griffin/Desktop/INST447_labs/lab_practice_CSVs/3-25-26/Maryland_Average_Wage_Per_Job_(in_Constant_2024_Dollars)__2014-2024_20260325.csv")
wages.columns # check the variables
wages.head()  # look at the top few rows
wages.tail()  # look at the bottom few rows
wages         # look at both, with a rows by column count

population = pd.read_csv("/Users/griffin/Desktop/INST447_labs/lab_practice_CSVs/3-25-26/Maryland_and_Jurisdictions_Population_Estimates_2020-2024.csv")
population.columns
population.head()

# First let's clean up the population data frame
# We want to make it match the wages, so we need to:
# 1. Get the year out of the time stamp
# 2. Change Jurisdiction to County
# 3. And let's drop the overall MARYLAND rows

# We'll explain this in more depth when we talk about time
# and transformations. But for now, just note that 
# the first line is a manual "check" that we can take an
# example string from the data and convert it into an integer
# year value. The second line applies this conversion to an
# entire column in the data frame, and assigns that new year
# value to a new column called "Year" (to match the wages
# data frame)
time.strptime("06/30/2020 12:00:00 AM", "%m/%d/%Y %H:%M:%S %p").tm_year
population["Year"] = population["Reporting period end date"].apply(lambda x: time.strptime(x, "%m/%d/%Y %H:%M:%S %p").tm_year)

# now let's peek again as a spot check
population.head()
population.tail()

# time to rename the columns
# you can pass a dictionary of "old name" : "new name" pairs
# to the DataFrame.rename() method
population = population.rename(columns = {"Jurisdiction" : "County"})

# one way to select just a few columns is by name:
population = population[["County", "Year", "Population"]]
population.head() # check the results

# finally, let's drop the rows for MARYLAND
# the method below is handy if you want to exclude from multiple
# values, so it's a good pattern to learn, though a little 
# overkill for this specific case
areas_to_exclude = ["MARYLAND"]
population = population[~population["County"].isin(areas_to_exclude)]
population.head() # check the result

# when we alter DataFrames, we often end up changing the index
# sometimes you can leverage the index for helpful things,
# but my preference is to keep the index as "neutral" as
# possible, which means "resetting" it whenever it gets
# altered

# if you leave out drop = True, the old index is added to the
# data frame as a new column
population = population.reset_index(drop = True)
population.head() # see how the index is "reset" to start at 0 again

#################################
# so now that population is cleaned up, let's deal with the wages

# first, we know that we don't care about "Date created" and we
# know we don't want the MARYLAND values, so let's drop these
# using a different method

# DataFrame.drop() returns a DataFrame, dropping columns or rows
wages = wages.drop(columns = ["Date created", "MARYLAND"]) 

## alternatively, DataFrame.pop() works similar to list.pop(),
## returning the removed column and altering the original DataFrame
## only works with single column names
# wages.pop("Date created") # this would return the "Date created column" and remove it from wages

wages.columns # check that the column drop worked
wages.head()

# now we need to reshape this data frame from "wide" to "long" format
# there is also a DataFrame.wide_to_long() method, but melt() is
# more powerful, and more comparable to pivot() going the other direction
# TRIVIA: melt() comes from the older `reshape2` package from R, which
#         used melt() and cast(), but those have been more recently
#         superceded in R by pivot_longer() and pivot_wider() in the
#         `tidyr` package
# this first one "melts" all of the columns except for the id_vars
wages_long1 = wages.melt(id_vars = "Year")
wages_long1

# alternatively, you can specify which columns to melt, but then
# the id_vars are left out
wages_long2 = wages.melt(value_vars = wages.columns[1:])
wages_long2

# you can also melt just some of the columns, which leaves out the
# columns you didn't include
# in other words:
#   id_vars = columns that you want to keep as columns (not melt)
#   value_vars = columns that you want to melt into "variable" and "value" columns
wages_long3 = wages.melt(id_vars = "Year", value_vars = ["Montgomery County", "Prince George's County"])
wages_long3

# if you don't want the generic "variable" and "value" column names,
# you can specify var_name (which replaces "variable") and value_name
# (which replaces "value")
wages_long = wages.melt(id_vars = "Year", var_name = "County", value_name = "Average Salary")

# let's confirm that we have gotten these data frames into 
# similar shapes, so that they can be merged
wages_long.head()
population.head()

# we want to merge on both County and Year
# but before we do, let's double-check that the values are
# going to match up
wages_long["County"].unique() # all of the observed County values

# we are looking for False's, which would indicate something that
# exists in one data frame but not the other
pd.Series(wages_long["County"].unique()).isin(population["County"])
pd.Series(population["County"].unique()).isin(wages_long["County"])

# for unique numeric arrays, you may need to explicitly
# convert to a Series first
pd.Series(wages_long["Year"].unique())
pd.Series(wages_long["Year"].unique()).isin(population["Year"])
pd.Series(population["Year"].unique()).isin(wages_long["Year"])

# so this helps us see that the wages data has several years
# that the population data does not (from 2014-2019)

# here's another way to see this with numbers, looking at
# ranges:
population["Year"].describe()
wages_long["Year"].describe()

# so let's look at how to merge or join these

# the `how` parameter specifies the type of join,
# where you can choose left, right, inner, outer, etc.
# see the help for pd.DataFrame.merge() for all the details
# the `on` parameter is where you pass the (matching) names
# of columns you are merging on
# note there are also `left_on` and `right_on` parameters
# you can use instead if the column names don't match
wage_pop_all = pd.merge(wages_long, population, how = "left",
                    on = ["County", "Year"])

# since the "left" data frame (wages_long) has more years
# than the "right" data set, and we are performing a "left" join,
# we end up with rows where we don't have a population value
len(wage_pop_all)
len(wages_long)
len(population)
wage_pop_all.head(20)

# we'll discuss this type of missing data later

# in the meantime, we could choose a right join or inner
# join to end up with just the data frame where we have
# matching values in both merged data frames 
wage_pop = pd.merge(wages_long, population, how = "inner",
                    on = ["County", "Year"])
len(wage_pop)
wage_pop.head(20)
wage_pop.describe()

# one more reshape for fun
# let's focus on MoCo and PG, and then "pivot" the data
# by year

counties_to_keep = ["Montgomery County", "Prince George's County"]
wage_pop_subset = wage_pop[wage_pop["County"].isin(counties_to_keep)].reset_index(drop = True)
wage_pop_subset

wages_wide = wage_pop_subset.pivot(columns = ["Year"],
                      index = ["County"],
                      values = ["Average Salary"])
wages_wide
