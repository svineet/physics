Physics
=======

A Physics Activity in kivy, for the kivy app challenge.


Setup
-----

```bash
pip install -r requirements.txt
```

And `python main.py`  
No hardware specific features. Only PC supported for now.


Introduction
------------

Physics is a playground for young learners to see how things work, and try out things that are hard to do in real world. Like drop a ball from a tower to see which lands first ;)
Newton's cradle, Galileo's Pisa experiment, and simple experiments like these can easily be made in this program.

I am a contributor to [Sugar Labs](http://sugarlabs.org/), an organization which develops Sugar, a learning environment which runs on 3 million laptops ("One laptop per child" initiative's XO range) worldwide in over 40 countries, including Australia, Uruguay, and a small(very small) part of India, and so many more countries.

[Physics](https://github.com/walterbender/physics) is a Sugar application which is much like this one. My app is inspired by Physics and thus named so too. I am also a [contributor](https://github.com/walterbender/physics/blob/master/NEWS) to the Activity, and the Activity is written in Box2d and pygame, so no code copying, written from scratch :)
P.S: Application == Activity in Sugar jargon

Go on, run it and have fun :)


Warning
-------

This stuff is experimental. There is no android support since cymunk doesn't work properly and there are inconsistencies between the pymunk and the cymunk api. This app was previously written for cymunk so all files have `cymunk.Space`, `cymunk.Poly`, `cymunk.Body`, etc. , but at the start its `import pymunk as cymunk`. 


What doesn't work:
------------------

* Triangles don't behave properly. I've looked into the issue, I couldn't find the problem. 


> Therefore the Master  
> acts without doing anything  
> and teaches without saying anything.  
> Things arise and she lets them come;  
> things disappear and she lets them go.  
> She has but doesn't possess,  
> acts but doesn't expect.  
> When her work is done, she forgets it.  
> That is why it lasts forever.  
> - _Tao Te Ching_ , Stephen Mitchell translation
