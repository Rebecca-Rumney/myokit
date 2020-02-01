<?
# Template for Chaste model header file.
#
# Variables:
#   class_name      A valid camel cased class name
#   model_name      A user friendly model name (arbitrary string)
#   time            The name of the time variable in cpp
#
?>#ifndef <?= class_name.upper() ?>_HPP_
#define <?= class_name.upper() ?>_HPP_

//! @file
//!
//! This source file was generated by Myokit
//!
//! Model: <?= model_name ?>
//!
//! <autogenerated>

#include "ChasteSerialization.hpp"
#include <boost/serialization/base_object.hpp>
#include "AbstractCardiacCell.hpp"
#include "AbstractStimulusFunction.hpp"

class <?= class_name ?> : public AbstractCardiacCell
{
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & archive, const unsigned int version)
    {
        archive & boost::serialization::base_object<AbstractCardiacCell >(*this);
    }

    //
    // Settable parameters and readable variables
    //

public:
    <?= class_name ?>(boost::shared_ptr<AbstractIvpOdeSolver> pSolver, boost::shared_ptr<AbstractStimulusFunction> pIntracellularStimulus);
    ~<?= class_name ?>();
    double GetIIonic(const std::vector<double>* pStateVariables=NULL);
    void EvaluateYDerivatives(double <?= time ?>, const std::vector<double>& rY, std::vector<double>& rDY);
};


// Needs to be included last
#include "SerializationExportWrapper.hpp"
CHASTE_CLASS_EXPORT(<?= class_name ?>)

namespace boost
{
    namespace serialization
    {
        template<class Archive>
        inline void save_construct_data(
            Archive & ar, const <?= class_name ?> * t, const unsigned int fileVersion)
        {
            const boost::shared_ptr<AbstractIvpOdeSolver> p_solver = t->GetSolver();
            const boost::shared_ptr<AbstractStimulusFunction> p_stimulus = t->GetStimulusFunction();
            ar << p_solver;
            ar << p_stimulus;
        }

        template<class Archive>
        inline void load_construct_data(
            Archive & ar, <?= class_name ?> * t, const unsigned int fileVersion)
        {
            boost::shared_ptr<AbstractIvpOdeSolver> p_solver;
            boost::shared_ptr<AbstractStimulusFunction> p_stimulus;
            ar >> p_solver;
            ar >> p_stimulus;
            ::new(t)<?= class_name ?>(p_solver, p_stimulus);
        }
    }
}

#endif // <?= class_name.upper() ?>_HPP_
