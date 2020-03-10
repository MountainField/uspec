# USpec


[USpec](https://github.com/MountainField/uspec) is a 'Domain Specific Language' (DSL) testing tool written in Python to test Python code in a 'Behavior-Driven Development' (BDD) mannar.

- Alomost the same grammar as [Rspec](https://rspec.info) 
- Alternative representaiotn of a test case of [unittest](https://docs.python.org/3/library/unittest.html). Since Uspec file can be tested by unittest, Developers can gradually migrate existing unittests to USpec.

## What is USpec?

### USpec has the alomost the same grammar as RSpec

Let's assume that [Bowling class](https://rspec.info) calculates the sum of game scores if there is no strikes and spares.

- `bowling.py`

    ```python
	class Bowling(object):
	    
	    def __init__(self):
	        self._score = 0
	    
	    def hit(self, pins):
	        self._score += pins
	
	    def score(self):
	        return self._score
    ```

For example, the instance of the Bowling class returns 80 for 20 same hit numbers 4, 4, ... , 4.
This example can be written in `bowling_spec.rb` by [Rspec file](https://rspec.info) which is the most common BDD tool.
Using [USpec](https://github.com/MountainField/uspec), we can write a spec Python file `bowling_spec.py` equivalent to `bowling_spec.rb` 

- `bowling_spec.rb`

	```ruby
	RSpec.describe Bowling, "#score" do
	    context "with no strikes or spares" do
	        it "sums the pin count for each roll" do
	            bowling = Bowling.new
	            20.times { bowling.hit(4) }
	            expect(bowling.score).to eq 80
	        end
	    end
	end
	```
	
- `bowling_spec.py`
	
	```python
	from uspec import description, context, it
	
	with description(Bowling, "#score"):
	    with context("with no strikes or spaces"):
	        @it("sums the pin count for each roll")
	        def _(self):
	            bowling = Bowling()
	            for i in range(20): bowling.hit(4)
	            self.assertEqual(bowling.score(), 80)
	```

### Uspec file is an alternative representation of unittest file

When a Uspec file is loaded by Python runtime, it generates a sub class of `unittest.TestCase` in that place.

- The equivalent test case of the USpec file `bowling_spec.py` above benerated by USpec is:

	```python
	import unittest
	class TestBowling_Score__WithNoStrikesOrSpaces(unittest.TestCase):
	    def test_sums_the_pin_count_for_each_roll(self):
	        bowling = Bowling()
	        for i in range(20):
	            bowling.hit(4)
	        self.assertEqual(bowling.score(), 80)
	```

### Uspec file can be tested by unittest

- Uspec file behaves as if it was written in unittest format, so it can be tested by unittest below:

	```
	$ python -m unittest -v bowling_spec.py 
	test0000: Bowling#score (with no strikes or spaces) sums the pin count for each roll (uspec.TestBowling#score) ... ok
	
	----------------------------------------------------------------------
	Ran 1 tests in 0.000s
	
	OK
	```

- Mix of Uspec files and unittest files can be also tested by unittest.
Assume that `test_baseball.py` is the traditional unittest file.
Since `bowling_spec.py` and` test_baseball.py` can be processed simultaneously by unittest, The total count of test cases becomes sum of test case of these files: 

	```
	$ python -m unittest -v bowling_spec.py   test_baseball.py
	test0000: Bowling#score (with no strikes or spaces) sums the pin count for each roll (uspec.TestBowling#score) ... ok
	test_game_countes (test_baseball.py.TestBaseball) ... ok
	
	----------------------------------------------------------------------
	Ran 2 tests in 0.000s
	
	OK
	```



Usage
-----




Author
------

- **Takahide Nogayama** - [Nogayama](https://github.com/nogayama)



License
-------

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details



Contributing
------------

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.


