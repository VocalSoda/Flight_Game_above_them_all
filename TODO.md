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

## Database & Data Layer (pham)
- [ ] Write function to connect to the airport database
- [ ] Write function to fetch N random airports from the database (filtering already exploded ones)
- [ ] Function to select 10 random airports from the database
- [ ] Function to display the 10 airports and their countries to the player
  - For this, we'd have it be like "KRYG, Kazakhstan (X)", where (X) denotes that the airport is infected
- [ ] Function to randomly choose 1–3 airports to "infect" (the ones the player must type)

## Game Logic (zeynab)
- [ ] Function to run a single round:
  - [ ] Show the 10 airports
  - [ ] Reveal which airports are infected
  - [ ] Prompt the player to type each infected airport name (Enter to submit)
  - [ ] Check if typed name matches the infected airport
  - [ ] Handle a timer / time limit per round (optional but nice)
  - [ ] Mark the airport as "exploded" on success
- [ ] Function to track score across rounds
- [ ] Function to check win condition (complete 5 rounds)

## game loop & io (maksym)
- [x] Main game loop that runs 5 rounds
- [x] After each round, print score / progress
- [x] After 5 rounds, display victory message
- [x] Handle game-over if player fails a round (optional)
- [x] Clean console output formatting (clear, readable airport list)
- [x] Input handling with Enter to submit each airport name
- [x] Case-insensitive matching for airport names (nice-to-have)
- [x] Test with a small seed dataset to verify game flow
- [ ] Add error handling (e.g., empty database, invalid input)