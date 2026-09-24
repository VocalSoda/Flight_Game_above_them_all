# TODO
If you guys don't know MD, make a [ ] a [x] when you've completed something.
You don't have to do it in this order, whatever order works is fine.

If you don't know how to do something, or if you have *any* questions please ask me !!!! 

### General Game Idea
This is gonna be a typing game, where we have 5 rounds.
Each round, we select 10 airports from the database, and display them like this:

```
---
  - [ICAO], Country
  - [ICAO], Country (x)
  - [ICAO], Country
  - [ICAO], Country
  - [ICAO], Country
  - [ICAO], Country (x)
  - [ICAO], Country
  - [ICAO], Country
---
```

The user then types the *icao* code of the infected airport, hits enter, and it gets marked as destroyed, and the airports are printed out again.
Then, we store the airport as destroyed, so that we don't show it again by accident.

The user will have a time limit per round, and if they're too slow they blow up and die or something.
Once there's no more infected airports, we increment the round counter, and get 10 more airports.

We'll also want a little intro message that explains the "lore", eg. `You are the lone soldier who must save the world from a virus that attacks only airports` or wtv.

### Project Structure
We can have everything in just 1 file.
The DB we'll use is the airports DB from our SQL course, but we'll want each of us to make a local copy of it, so we don't break the original (in-case we need a backup).

## (pham)

## (zeynab)
1. create sql script which creates a table containing save-files.
pkey: number,
name: varchar,
score: varchar,
did_win: boolean,
2. when loading the program, fetch the savefiles, display highscores
3. after the user finishes a game, ask them for their name, and store the name and score in the database.
4. make sure that the table is only created if it does not already exist
5. explain how to source the `.sql` file into the project so that the teachers and other developers can update their local databases

## (maksym)