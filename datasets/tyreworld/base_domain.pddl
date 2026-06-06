(define (domain tyreworld)
  (:requirements :typing)
  (:types 
    object
    tool wheel nut
    container hubect
  )
  (:predicates 
    (open ?x)
    (closed ?x)
    (have ?x)
    (in ?x ?y)
    (loose ?x ?y)
    (tight ?x ?y)
    (unlocked ?x)
    (on-ground ?x)
    (not-on-ground ?x)
    (inflated ?x)
    (not-inflated ?x)
    (fastened ?x)
    (unfastened ?x)
    (free ?x)
    (on ?x ?y)
    (intact ?x)
  )


  (:action open)
  (:action close)
  (:action fetch)
  (:action put-away)
  (:action loosen)
  (:action tighten)
  (:action jack-up)
  (:action jack-down)
  (:action undo)
  (:action do-up)
  (:action remove-wheel)
  (:action put-on-wheel)
  (:action inflate)
)



