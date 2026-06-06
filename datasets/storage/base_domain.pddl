(define (domain storage)
  (:requirements :typing)
  (:types 
    hoist surface place area - object
    container depot - place
    storearea transitarea - area
    area crate - surface
  )

  (:predicates 
    (clear ?s)
    (in ?x ?p)
    (available ?h)
    (lifting ?h ?c)
    (at ?h ?a)
    (on ?c ?s)
    (connected ?a1 ?a2)
    (compatible ?c1 ?c2)
  )

  (:action lift)
  (:action drop)
  (:action move)
  (:action go-out)
  (:action go-in)
)
