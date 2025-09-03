import Image from "next/image";

export default function WhenNeedPlumber() {
  return (
    <section className="bg-white pb-12 mx-auto space-y-10 text-gray-800">
      <div>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          When do you need a plumber?
        </h2>
        <p className="mb-4">
          All projects that require work with water, pipes and drainage require
          you to bring in a plumber to do the job. You can either find a plumber
          yourself for a specific project, or you can get help from a contractor
          to hire a plumber as part of a larger project.
        </p>

        <div className="mb-2">
          <Image
            src="/assets/my-tender/35.svg"
            alt="Installing shower mixer"
            width={600}
            height={140}
            className="rounded-md"
          />
        </div>

        <p className="text-sm text-gray-600">
          You can install the shower mixer yourself if a shut-off valve is
          installed and you have the option of turning off the water, but we
          always recommend using a professional. Then you are safe should
          something happen.
        </p>
      </div>

      {/* Section: Renovate the bathroom */}
      <div>
        <h3 className="font-semibold text-lg text-gray-900 mb-2">
          Renovate the bathroom
        </h3>
        <p className="mb-2">
          A bathroom renovation will require plumbing. Regardless of whether it
          is a total renovation or a surface renovation, a certified plumber
          should do the job.
        </p>
        <p className="mb-2">
          This is because the scope of damage in the event of any errors in a
          bathroom is much greater than in other projects, for example if a leak
          occurs. But also because work without certification on water and
          sewage will not be covered by insurance should damage occur.
        </p>
        <a href="#" className="text-teal-700 underline">
          You can read more about renovating a bathroom here
        </a>
      </div>

      {/* Section: Pusse opp kjøkken */}
      <div>
        <h3 className="font-semibold text-lg text-gray-900 mb-2">Pusse opp kjøkken</h3>
        <p className="mb-2">
          Oppussing av kjøkken krever ofte arbeid på vann og avløp, og da trenger du en rørlegger.
        </p>
        <p className="mb-2">
          Omfanget på arbeidet vil ofte avhenge av hvor store endringer som skal gjøres, og hvordan det påvirker det eksisterende oppsettet for vann- og avløpsrør.
        </p>
        <a href="#" className="text-teal-700 underline">
          Du kan lese mer om å pusse opp kjøkken her
        </a>
      </div>

      {/* Highlight Banner */}
      <div className="relative p-6 rounded-md text-center">
        <Image
          src="/assets/my-tender/36.svg"
          alt="Underline style"
          width={600}
          height={30}
          className="absolute left-1/2 top-5 -translate-x-1/2"
        />
        <p className="text-lg font-medium relative z-10">
          A total renovation involves in-depth rehabilitation and change of what
          lies beneath visible surfaces, and then it is important to use skilled
          craftsmen to get a quality-assured result.
        </p>
      </div>

      {/* Section: New construction */}
      <div>
        <h3 className="font-semibold text-lg text-gray-900 mb-2">
          New construction
        </h3>
        <p className="mb-2">
          New buildings intended for permanent residence will often require work
          on rooms that have water and drainage systems. This can be a house, an
          apartment, outbuilding, extension or a rental unit.
        </p>
        <a href="#" className="text-teal-700 underline">
          Read more about building a house here
        </a>
      </div>
    </section>
  );
}
