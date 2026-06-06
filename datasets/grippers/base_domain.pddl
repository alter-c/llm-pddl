(define (domain grippers)
  (:requirements :strips :typing) 
  (:types room object robot gripper)
  (:predicates 
    (at-robby ?r ?x)
    (at ?o ?x)
    (free ?r ?g)
    (carry ?r ?o ?g)
  )

  (:action move)
  (:action pick)
  (:action drop)
)