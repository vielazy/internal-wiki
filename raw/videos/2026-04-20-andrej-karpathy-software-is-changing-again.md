---
title: "Andrej Karpathy: Software Is Changing (Again)"
url: "https://www.youtube.com/watch?v=LCEmiRjPEtQ"
discovered: "2026-04-20"
topic: "AI Agents"
source_type: "youtube"
---

# Andrej Karpathy: Software Is Changing (Again)

## Transcript

[1.12s] Please welcome former director of AI

[4.00s] Tesla Andre Carpathy.

[7.17s] [Music]

[11.44s] Hello.

[14.77s] [Music]

[19.04s] Wow, a lot of people here. Hello.

[22.80s] Um, okay. Yeah. So I'm excited to be

[24.80s] here today to talk to you about software

[27.20s] in the era of AI. And I'm told that many

[30.56s] of you are students like bachelors,

[32.56s] masters, PhD and so on. And you're about

[34.40s] to enter the industry. And I think it's

[36.40s] actually like an extremely unique and

[37.76s] very interesting time to enter the

[38.96s] industry right now. And I think

[41.36s] fundamentally the reason for that is

[43.04s] that um software is changing uh again.

[47.60s] And I say again because I actually gave

[49.92s] this talk already. Um but the problem is

[52.56s] that software keeps changing. So I

[54.08s] actually have a lot of material to

[55.20s] create new talks and I think it's

[56.72s] changing quite fundamentally. I think

[58.16s] roughly speaking software has not

[60.32s] changed much on such a fundamental level

[62.00s] for 70 years. And then it's changed I

[64.56s] think about twice quite rapidly in the

[66.88s] last few years. And so there's just a

[68.56s] huge amount of work to do a huge amount

[69.84s] of software to write and rewrite. So

[72.32s] let's take a look at maybe the realm of

[74.16s] software. So if we kind of think of this

[76.08s] as like the map of software this is a

[77.76s] really cool tool called map of GitHub.

[80.00s] Um this is kind of like all the software

[81.92s] that's written. Uh these are

[83.36s] instructions to the computer for

[84.64s] carrying out tasks in the digital space.

[86.40s] So if you zoom in here, these are all

[88.00s] different kinds of repositories and this

[90.08s] is all the code that has been written.

[91.68s] And a few years ago I kind of observed

[93.60s] that um software was kind of changing

[95.84s] and there was kind of like a new type of

[97.76s] software around and I called this

[99.68s] software 2.0 at the time and the idea

[102.32s] here was that software 1.0 is the code

[104.64s] you write for the computer. Software 2.0

[106.80s] know are basically neural networks and

[108.80s] in particular the weights of a neural

[110.32s] network and you're not writing this code

[113.28s] directly you are most you are more kind

[115.44s] of like tuning the data sets and then

[116.88s] you're running an optimizer to create to

[118.40s] create the parameters of this neural net

[120.88s] and I think like at the time neural nets

[122.56s] were kind of seen as like just a

[123.60s] different kind of classifier like a

[124.80s] decision tree or something like that and

[126.24s] so I think it was kind of like um I

[129.04s] think this framing was a lot more

[130.24s] appropriate and now actually what we

[132.24s] have is kind of like an equivalent of

[133.52s] GitHub in the realm of software 2.0 And

[135.76s] I think the hugging face is basically

[138.08s] equivalent of GitHub in software 2.0.

[140.72s] And there's also model atlas and you can

[142.40s] visualize all the code written there. In

[144.24s] case you're curious, by the way, the

[145.44s] giant circle, the point in the middle,

[148.32s] uh these are the parameters of flux, the

[150.88s] image generator. And so anytime someone

[152.88s] tunes a on top of a flux model, you

[154.96s] basically create a git commit uh in this

[157.12s] space and uh you create a different kind

[159.12s] of a image generator. So basically what

[161.60s] we have is software 1.0 is the computer

[163.60s] code that programs a computer. Software

[165.92s] 2.0 are the weights which program neural

[168.72s] networks. Uh and here's an example of

[170.72s] Alexet image recognizer neural network.

[173.52s] Now so far all of the neural networks

[175.04s] that we've been familiar with until

[176.40s] recently where kind of like fixed

[178.16s] function computers image to categories

[181.68s] or something like that. And I think

[183.44s] what's changed and I think is a quite

[185.20s] fundamental change is that neural

[186.72s] networks became programmable with large

[189.60s] language models. And so I I see this as

[192.16s] quite new, unique. It's a new kind of a

[194.96s] computer and uh so in my mind it's uh

[198.00s] worth giving it a new designation of

[199.60s] software 3.0. And basically your prompts

[202.16s] are now programs that program the LLM.

[205.68s] And uh remarkably uh these uh prompts

[208.32s] are written in English. So it's kind of

[210.40s] a very interesting programming language.

[213.60s] Um so maybe uh to summarize the

[216.80s] difference if you're doing sentiment

[217.92s] classification for example you can

[219.44s] imagine writing some uh amount of Python

[222.48s] to to basically do sentiment

[224.24s] classification or you can train a neural

[226.00s] net or you can prompt a large language

[227.84s] model. Uh so here this is a few short

[230.00s] prompt and you can imagine changing it

[231.28s] and programming the computer in a

[232.80s] slightly different way. So basically we

[234.64s] have software 1.0 software 2.0 and I

[237.60s] think we're seeing maybe you've seen a

[239.68s] lot of GitHub code is not just like code

[241.92s] anymore. there's a bunch of like English

[243.52s] interspersed with code and so I think

[245.44s] kind of there's a growing category of

[247.36s] new kind of code. So not only is it a

[249.20s] new programming paradigm, it's also

[250.88s] remarkable to me that it's in our native

[252.72s] language of English. And so when this

[254.88s] blew my mind a few uh I guess years ago

[257.92s] now I tweeted this and um I think it

[260.88s] captured the attention of a lot of

[261.92s] people and this is my currently pinned

[263.20s] tweet uh is that remarkably we're now

[265.36s] programming computers in English. Now,

[268.16s] when I was at uh Tesla, um we were

[271.60s] working on the uh autopilot and uh we

[274.96s] were trying to get the car to drive and

[277.44s] I sort of showed this slide at the time

[279.92s] where you can imagine that the inputs to

[281.68s] the car are on the bottom and they're

[283.20s] going through a software stack to

[284.64s] produce the steering and acceleration

[287.04s] and I made the observation at the time

[288.56s] that there was a ton of C++ code around

[291.12s] in the autopilot which was the software

[292.72s] 1.0 code and then there was some neural

[294.48s] nets in there doing image recognition

[296.96s] and uh I kind of observed that over time

[298.80s] as we made the autopilot better

[300.88s] basically the neural network grew in

[302.72s] capability and size and in addition to

[305.84s] that all the C++ code was being deleted

[308.56s] and kind of like was um and a lot of the

[312.08s] kind of capabilities and functionality

[314.56s] that was originally written in 1.0 was

[316.48s] migrated to 2.0. So as an example, a lot

[319.04s] of the stitching up of information

[320.72s] across images from the different cameras

[322.64s] and across time was done by a neural

[324.96s] network and we were able to delete a lot

[326.48s] of code and so the software 2.0 stack

[329.84s] quite literally ate through the software

[332.56s] stack of the autopilot. So I thought

[334.16s] this was really remarkable at the time

[335.68s] and I think we're seeing the same thing

[337.04s] again where uh basically we have a new

[339.36s] kind of software and it's eating through

[340.80s] the stack. We have three completely

[342.48s] different programming paradigms and I

[344.40s] think if you're entering the industry

[345.60s] it's a very good idea to be fluent in

[347.36s] all of them because they all have slight

[349.36s] pros and cons and you may want to

[350.80s] program some functionality in 1.0 or 2.0

[353.12s] or 3.0. Are you going to train

[354.40s] neurallet? Are you going to just prompt

[355.60s] an LLM? Should this be a piece of code

[357.44s] that's explicit etc. So we all have to

[359.36s] make these decisions and actually

[360.56s] potentially uh fluidly trans transition

[363.52s] between these paradigms. So what I

[366.80s] wanted to get into now is first I want

[369.76s] to in the first part talk about LLMs and

[371.76s] how to kind of like think of this new

[373.52s] paradigm and the ecosystem and what that

[375.12s] looks like. Uh like what are what is

[377.44s] this new computer? What does it look

[378.72s] like and what does the ecosystem look

[380.24s] like? Um I was struck by this quote from

[383.76s] Anduring actually uh many years ago now

[385.76s] I think and I think Andrew is going to

[387.52s] be speaking right after me. Uh but he

[389.44s] said at the time AI is the new

[390.64s] electricity and I do think that it um

[393.36s] kind of captures something very

[394.64s] interesting in that LLMs certainly feel

[396.72s] like they have properties of utilities

[398.96s] right now. So

[401.60s] um LLM labs like OpenAI, Gemini,

[404.24s] Enthropic etc. They spend capex to train

[407.12s] the LLMs and this is kind of equivalent

[408.88s] to building out a grid and then there's

[411.12s] opex to serve that intelligence over

[413.04s] APIs to all of us and this is done

[416.40s] through metered access where we pay per

[418.64s] million tokens or something like that

[420.40s] and we have a lot of demands that are

[421.92s] very utility- like demands out of this

[423.92s] API we demand low latency high uptime

[426.24s] consistent quality etc. In electricity,

[428.96s] you would have a transfer switch. So you

[430.80s] can transfer your electricity source

[432.40s] from like grid and solar or battery or

[434.40s] generator. In LLM, we have maybe open

[436.80s] router and easily switch between the

[438.56s] different types of LLMs that exist.

[440.64s] Because the LLM are software, they don't

[443.04s] compete for physical space. So it's okay

[445.04s] to have basically like six electricity

[446.72s] providers and you can switch between

[448.16s] them, right? Because they don't compete

[449.84s] in such a direct way. And I think what's

[451.92s] also a little fascinating and we saw

[453.68s] this in the last few days actually a lot

[456.48s] of the LLMs went down and people were

[458.80s] kind of like stuck and unable to work.

[461.12s] And uh I think it's kind of fascinating

[462.48s] to me that when the state-of-the-art

[463.76s] LLMs go down, it's actually kind of like

[465.76s] an intelligence brownout in the world.

[467.76s] It's kind of like when the voltage is

[469.36s] unreliable in the grid and uh the planet

[472.08s] just gets dumber the more reliance we

[475.12s] have on these models, which already is

[476.72s] like really dramatic and I think will

[478.40s] continue to grow. But LLM's don't only

[480.80s] have properties of utilities. I think

[482.24s] it's also fair to say that they have

[483.52s] some properties of fabs. And the reason

[486.48s] for this is that the capex required for

[489.52s] building LLM is actually quite large. Uh

[492.24s] it's not just like building some uh

[494.32s] power station or something like that,

[495.92s] right? You're investing a huge amount of

[497.60s] money and I think the tech tree and uh

[500.00s] for the technology is growing quite

[502.48s] rapidly. So we're in a world where we

[504.40s] have sort of deep tech trees, research

[506.96s] and development secrets that are

[508.96s] centralizing inside the LLM labs. Um and

[512.40s] but I think the analogy muddies a little

[514.24s] bit also because as I mentioned this is

[516.24s] software and software is a bit less

[518.16s] defensible because it is so malleable.

[520.96s] And so um I think it's just an

[523.04s] interesting kind of thing to think about

[524.32s] potentially. There's many analogy

[526.64s] analogies you can make like a 4

[528.16s] nanometer process node maybe is

[529.60s] something like a cluster with certain

[531.04s] max flops. You can think about when

[533.04s] you're use when you're using Nvidia GPUs

[534.80s] and you're only doing the software and

[536.08s] you're not doing the hardware. That's

[537.12s] kind of like the fabless model. But if

[539.12s] you're actually also building your own

[540.32s] hardware and you're training on TPUs if

[542.00s] you're Google, that's kind of like the

[543.28s] Intel model where you own your fab. So I

[545.20s] think there's some analogies here that

[546.40s] make sense. But actually I think the

[548.24s] analogy that makes the most sense

[549.76s] perhaps is that in my mind LLM have very

[552.48s] strong kind of analogies to operating

[555.28s] systems. Uh in that this is not just

[557.76s] electricity or water. It's not something

[559.52s] that comes out of the tap as a

[560.96s] commodity. uh this is these are now

[562.96s] increasingly complex software ecosystems

[565.92s] right so uh they're not just like simple

[568.72s] commodities like electricity and it's

[570.88s] kind of interesting to me that the

[572.00s] ecosystem is shaping in a very similar

[573.92s] kind of way where you have a few closed

[576.16s] source providers like Windows or Mac OS

[578.56s] and then you have an open source

[579.84s] alternative like Linux and I think for u

[582.72s] neural for LLMs as well we have a kind

[585.52s] of a few competing closed source

[587.52s] providers and then maybe the llama

[589.20s] ecosystem is currently like maybe a

[591.44s] close approximation to something that

[593.12s] may grow into something like Linux.

[595.12s] Again, I think it's still very early

[596.48s] because these are just simple LLMs, but

[598.16s] we're starting to see that these are

[599.60s] going to get a lot more complicated.

[601.12s] It's not just about the LLM itself. It's

[602.80s] about all the tool use and the

[603.92s] multiodalities and how all of that

[605.52s] works. And so when I sort of had this

[607.28s] realization a while back, I tried to

[609.36s] sketch it out and it kind of seemed to

[611.20s] me like LLMs are kind of like a new

[612.80s] operating system, right? So the LLM is a

[615.84s] new kind of a computer. It's sitting

[617.60s] it's kind of like the CPU equivalent. uh

[619.76s] the context windows are kind of like the

[621.52s] memory and then the LLM is orchestrating

[624.40s] memory and compute uh for problem

[626.64s] solving um using all of these uh

[629.84s] capabilities here and so definitely if

[632.64s] you look at it looks very much like

[634.32s] operating system from that perspective.

[636.48s] Um, a few more analogies. For example,

[638.88s] if you want to download an app, say I go

[641.20s] to VS Code and I go to download, you can

[643.68s] download VS Code and you can run it on

[646.24s] Windows, Linux or or Mac in the same way

[650.16s] as you can take an LLM app like cursor

[653.12s] and you can run it on GPT or cloud or

[655.52s] Gemini series, right? It's just a drop

[657.44s] down. So, it's kind of like similar in

[659.04s] that way as well.

[660.72s] uh more analogies that I think strike me

[662.40s] is that we're kind of like in this

[664.32s] 1960sish

[665.92s] era where LLM compute is still very

[669.04s] expensive for this new kind of a

[670.72s] computer and that forces the LLMs to be

[673.44s] centralized in the cloud and we're all

[675.84s] just uh sort of thing clients that

[678.40s] interact with it over the network and

[680.32s] none of us have full utilization of

[682.08s] these computers and therefore it makes

[684.16s] sense to use time sharing where we're

[686.40s] all just you know a dimension of the

[688.32s] batch when they're running the computer

[690.00s] in the cloud. And this is very much what

[692.00s] computers used to look like at during

[693.44s] this time. The operating systems were in

[695.04s] the cloud. Everything was streamed

[696.16s] around and there was batching. And so

[699.60s] the p the personal computing revolution

[701.52s] hasn't happened yet because it's just

[702.96s] not economical. It doesn't make sense.

[704.56s] But I think some people are trying. And

[706.72s] it turns out that Mac minis, for

[708.40s] example, are a very good fit for some of

[710.40s] the LLMs because it's all if you're

[712.32s] doing batch one inference, this is all

[713.84s] super memory bound. So this actually

[715.36s] works.

[716.88s] And uh I think these are some early

[718.72s] indications maybe of personal computing.

[720.40s] Uh but this hasn't really happened yet.

[722.08s] It's not clear what this looks like.

[723.52s] Maybe some of you get to invent what

[725.20s] what this is or how it works or uh what

[728.08s] this should what this should be. Maybe

[730.32s] one more analogy that I'll mention is

[732.16s] whenever I talk to Chach or some LLM

[734.56s] directly in text, I feel like I'm

[736.48s] talking to an operating system through

[738.40s] the terminal. Like it's just it's it's

[741.04s] text. It's direct access to the

[742.64s] operating system. And I think a guey

[744.72s] hasn't yet really been invented in like

[746.72s] a general way like should chatt have a

[749.68s] guey like different than just a tech

[751.44s] bubbles. Uh certainly some of the apps

[753.44s] that we're going to go into in a bit

[755.36s] have guey but there's no like guey

[758.48s] across all the tasks if that makes

[760.24s] sense. Um there are some ways in which

[763.44s] LLMs are different from kind of

[765.52s] operating systems in some fairly unique

[767.44s] way and from early computing. And I

[769.84s] wrote about uh this one particular

[772.88s] property that strikes me as very

[774.24s] different uh this time around. It's that

[777.12s] LLMs like flip they flip the direction

[779.84s] of technology diffusion uh that is

[782.00s] usually uh present in technology. So for

[785.36s] example with electricity, cryptography,

[787.04s] computing, flight, internet, GPS, lots

[789.12s] of new transformative technologies that

[790.64s] have not been around. Typically it is

[792.32s] the government and corporations that are

[794.32s] the first users because it's new and

[796.72s] expensive etc. and it only later

[798.72s] diffuses to consumer. Uh, but I feel

[800.72s] like LLMs are kind of like flipped

[802.08s] around. So maybe with early computers,

[804.00s] it was all about ballistics and military

[806.00s] use, but with LLMs, it's all about how

[809.04s] do you boil an egg or something like

[810.32s] that. This is certainly like a lot of my

[812.00s] use. And so it's really fascinating to

[813.60s] me that we have a new magical computer

[815.60s] and it's like helping me boil an egg.

[817.36s] It's not helping the government do

[818.88s] something really crazy like some

[820.72s] military ballistics or some special

[822.16s] technology. Indeed, corporations are

[823.84s] governments are lagging behind the

[825.12s] adoption of all of us, of all of these

[827.20s] technologies. So, it's just backwards

[828.96s] and I think it informs maybe some of the

[830.48s] uses of how we want to use this

[832.40s] technology or like where are some of the

[833.60s] first apps and so on.

[836.08s] So, in summary so far, LLM labs LLMs. I

[841.04s] think it's accurate language to use, but

[843.68s] LLMs are complicated operating systems.

[846.48s] They're circa 1960s in computing and

[848.56s] we're redoing computing all over again.

[850.24s] and they're currently available via time

[851.84s] sharing and distributed like a utility.

[853.84s] What is new and unprecedented is that

[856.00s] they're not in the hands of a few

[857.36s] governments and corporations. They're in

[858.88s] the hands of all of us because we all

[860.24s] have a computer and it's all just

[861.60s] software and Chaship was beamed down to

[864.32s] our computers like billions of people

[866.64s] like instantly and overnight and this is

[868.32s] insane. Uh and it's kind of insane to me

[870.88s] that this is the case and now it is our

[873.28s] time to enter the industry and program

[874.96s] these computers. This is crazy. So I

[877.28s] think this is quite remarkable. Before

[879.68s] we program LLMs, we have to kind of like

[882.08s] spend some time to think about what

[883.52s] these things are. And I especially like

[885.84s] to kind of talk about their psychology.

[888.32s] So the way I like to think about LLMs is

[890.48s] that they're kind of like people

[891.52s] spirits. Um they are stoastic

[894.08s] simulations of people. Um and the

[896.40s] simulator in this case happens to be an

[898.00s] auto reggressive transformer. So

[899.84s] transformer is a neural net. Uh it's and

[902.72s] it just kind of like is goes on the

[904.80s] level of tokens. It goes chunk chunk

[906.48s] chunk chunk chunk. And there's an almost

[908.32s] equal amount of compute for every single

[910.16s] chunk. Um and um this simulator of

[914.72s] course is is just is basically there's

[916.96s] some weights involved and we fit it to

[919.04s] all of text that we have on the internet

[920.48s] and so on. And you end up with this kind

[922.16s] of a simulator and because it is trained

[924.24s] on humans, it's got this emergent

[926.24s] psychology that is humanlike. So the

[928.40s] first thing you'll notice is of course

[930.64s] uh LLM have encyclopedic knowledge and

[932.56s] memory. uh and they can remember lots of

[934.64s] things, a lot more than any single

[936.08s] individual human can because they read

[937.60s] so many things. It's it actually kind of

[939.84s] reminds me of this movie Rainman, which

[941.68s] I actually really recommend people

[943.04s] watch. It's an amazing movie. I love

[944.48s] this movie. Um and Dustin Hoffman here

[946.72s] is an autistic savant who has almost

[949.20s] perfect memory. So, he can read a he can

[951.60s] read like a phone book and remember all

[953.28s] of the names and phone numbers. And I

[955.36s] kind of feel like LM are kind of like

[957.20s] very similar. They can remember Shaw

[958.96s] hashes and lots of different kinds of

[960.40s] things very very easily. So they

[962.48s] certainly have superpowers in some set

[964.40s] in some respects. But they also have a

[966.24s] bunch of I would say cognitive deficits.

[968.80s] So they hallucinate quite a bit. Um and

[971.76s] they kind of make up stuff and don't

[973.12s] have a very good uh sort of internal

[975.28s] model of self-nowledge, not sufficient

[977.68s] at least. And this has gotten better but

[979.36s] not perfect. They display jagged

[981.60s] intelligence. So they're going to be

[982.80s] superhuman in some problems solving

[984.48s] domains. And then they're going to make

[986.00s] mistakes that basically no human will

[987.68s] make. like you know they will insist

[989.92s] that 9.11 is greater than 9.9 or that

[992.56s] there are two Rs in strawberry these are

[994.24s] some famous examples but basically there

[996.16s] are rough edges that you can trip on so

[998.88s] that's kind of I think also kind of

[1000.32s] unique um they also kind of suffer from

[1003.28s] entrograde amnesia um so uh and I think

[1006.88s] I'm alluding to the fact that if you

[1008.08s] have a co-orker who joins your

[1009.28s] organization this co-orker will over

[1011.44s] time learn your organization and uh they

[1014.16s] will understand and gain like a huge

[1015.92s] amount of context on the organization

[1017.76s] and they go home and they sleep and they

[1019.60s] consolidate knowledge and they develop

[1021.12s] expertise over time. LLMs don't natively

[1023.44s] do this and this is not something that

[1024.64s] has really been solved in the R&D of

[1026.40s] LLM. I think um and so context windows

[1029.28s] are really kind of like working memory

[1030.56s] and you have to sort of program the

[1032.00s] working memory quite directly because

[1033.60s] they don't just kind of like get smarter

[1035.04s] by uh by default and I think a lot of

[1037.04s] people get tripped up by the analogies

[1039.04s] uh in this way. Uh in popular culture I

[1042.24s] recommend people watch these two movies

[1043.92s] uh Momento and 51st dates. In both of

[1046.08s] these movies, the protagonists, their

[1047.76s] weights are fixed and their context

[1049.84s] windows gets wiped every single morning

[1052.16s] and it's really problematic to go to

[1054.24s] work or have relationships when this

[1055.76s] happens and this happens to all the

[1057.52s] time. I guess one more thing I would

[1059.60s] point to is security kind of related

[1062.32s] limitations of the use of LLM. So for

[1064.32s] example, LLMs are quite gullible. Uh

[1066.40s] they are susceptible to prompt injection

[1068.24s] risks. They might leak your data etc.

[1070.80s] And so um and there's many other

[1072.80s] considerations uh security related. So,

[1075.28s] so basically long story short, you have

[1077.52s] to load your you have to load your you

[1080.00s] have to simultaneously think through

[1081.28s] this superhuman thing that has a bunch

[1083.20s] of cognitive deficits and issues. How do

[1085.44s] we and yet they are extremely like

[1087.76s] useful and so how do we program them and

[1090.64s] how do we work around their deficits and

[1092.40s] enjoy their superhuman powers.

[1095.76s] So what I want to switch to now is talk

[1097.44s] about the opportunities of how do we use

[1098.96s] these models and what are some of the

[1100.72s] biggest opportunities. This is not a

[1102.40s] comprehensive list just some of the

[1103.52s] things that I thought were interesting

[1104.64s] for this talk. The first thing I'm kind

[1106.88s] of excited about is what I would call

[1109.28s] partial autonomy apps. So for example,

[1112.16s] let's work with the example of coding.

[1114.24s] You can certainly go to chacht directly

[1116.56s] and you can start copy pasting code

[1118.08s] around and copyping bug reports and

[1120.96s] stuff around and getting code and copy

[1122.40s] pasting everything around. Why would you

[1124.16s] why would you do that? Why would you go

[1125.44s] directly to the operating system? It

[1127.12s] makes a lot more sense to have an app

[1128.48s] dedicated for this. And so I think many

[1130.72s] of you uh use uh cursor. I do as well.

[1133.76s] And uh cursor is kind of like the thing

[1136.32s] you want instead. You don't want to just

[1137.76s] directly go to the chash apt. And I

[1139.76s] think cursor is a very good example of

[1141.44s] an early LLM app that has a bunch of

[1143.76s] properties that I think are um useful

[1146.16s] across all the LLM apps. So in

[1148.00s] particular, you will notice that we have

[1149.68s] a traditional interface that allows a

[1152.00s] human to go in and do all the work

[1153.84s] manually just as before. But in addition

[1156.48s] to that, we now have this LLM

[1157.84s] integration that allows us to go in

[1159.36s] bigger chunks. And so some of the

[1161.92s] properties of LLM apps that I think are

[1163.52s] shared and useful to point out. Number

[1165.84s] one, the LLMs basically do a ton of the

[1168.08s] context management. Um, number two, they

[1171.20s] orchestrate multiple calls to LLMs,

[1173.20s] right? So in the case of cursor, there's

[1174.96s] under the hood embedding models for all

[1176.96s] your files, the actual chat models,

[1179.20s] models that apply diffs to the code, and

[1181.84s] this is all orchestrated for you. A

[1183.92s] really big one that uh I think also

[1186.08s] maybe not fully appreciated always is

[1188.48s] application specific uh GUI and the

[1190.48s] importance of it. Um because you don't

[1193.12s] just want to talk to the operating

[1194.56s] system directly in text. Text is very

[1196.56s] hard to read, interpret, understand and

[1199.04s] also like you don't want to take some of

[1200.48s] these actions natively in text. So it's

[1203.12s] much better to just see a diff as like

[1205.04s] red and green change and you can see

[1206.80s] what's being added is subtracted. It's

[1208.48s] much easier to just do command Y to

[1210.24s] accept or command N to reject. I

[1211.92s] shouldn't have to type it in text,

[1213.12s] right? So, a guey allows a human to

[1215.52s] audit the work of these fallible systems

[1217.84s] and to go faster. I'm going to come back

[1220.00s] to this point a little bit uh later as

[1221.76s] well. And the last kind of feature I

[1223.84s] want to point out is that there's what I

[1225.20s] call the autonomy slider. So, for

[1227.68s] example, in cursor, you can just do tap

[1229.44s] completion. You're mostly in charge. You

[1231.52s] can select a chunk of code and command K

[1233.60s] to change just that chunk of code. You

[1236.00s] can do command L to change the entire

[1237.92s] file. Or you can do command I which just

[1240.40s] you know let it rip do whatever you want

[1242.16s] in the entire repo and that's the sort

[1244.08s] of full autonomy agent agentic version

[1246.40s] and so you are in charge of the autonomy

[1248.32s] slider and depending on the complexity

[1250.16s] of the task at hand you can uh tune the

[1253.04s] amount of autonomy that you're willing

[1254.32s] to give up uh for that task maybe to

[1257.12s] show one more example of a fairly

[1258.56s] successful LLM app uh perplexity um it

[1263.04s] also has very similar features to what

[1264.64s] I've just pointed out to in cursor uh it

[1267.20s] packages up a lot of the information. It

[1268.72s] orchestrates multiple LLMs. It's got a

[1270.96s] GUI that allows you to audit some of its

[1273.44s] work. So, for example, it will site

[1275.60s] sources and you can imagine inspecting

[1277.28s] them. And it's got an autonomy slider.

[1278.96s] You can either just do a quick search or

[1280.64s] you can do research or you can do deep

[1282.32s] research and come back 10 minutes later.

[1284.32s] So, this is all just varying levels of

[1285.68s] autonomy that you give up to the tool.

[1287.68s] So, I guess my question is I feel like a

[1290.16s] lot of software will become partially

[1292.00s] autonomous. I'm trying to think through

[1293.52s] like what does that look like? And for

[1295.28s] many of you who maintain products and

[1296.96s] services, how are you going to make your

[1298.96s] products and services partially

[1300.24s] autonomous? Can an LLM see everything

[1302.72s] that a human can see? Can an LLM act in

[1305.12s] all the ways that a human could act? And

[1307.04s] can humans supervise and stay in the

[1309.44s] loop of this activity? Because again,

[1310.88s] these are fallible systems that aren't

[1312.32s] yet perfect. And what does a diff look

[1314.88s] like in Photoshop or something like

[1316.56s] that? You know, and also a lot of the

[1318.80s] traditional software right now, it has

[1320.08s] all these switches and all this kind of

[1321.84s] stuff that's all designed for human. All

[1323.36s] of this has to change and become

[1324.72s] accessible to LLMs.

[1327.76s] So, one thing I want to stress with a

[1329.52s] lot of these LLM apps that I'm not sure

[1331.12s] gets as much attention as it should is

[1334.24s] um we we're now kind of like cooperating

[1336.80s] with AIS and usually they are doing the

[1338.64s] generation and we as humans are doing

[1340.16s] the verification. It is in our interest

[1342.56s] to make this loop go as fast as

[1344.48s] possible. So, we're getting a lot of

[1345.76s] work done. There are two major ways that

[1348.00s] I think uh this can be done. Number one,

[1350.40s] you can speed up verification a lot. Um,

[1352.72s] and I think guies, for example, are

[1354.24s] extremely important to this because a

[1356.08s] guey utilizes your computer vision GPU

[1359.28s] in all of our head. Reading text is

[1361.36s] effortful and it's not fun, but looking

[1363.20s] at stuff is fun and it's it's just a

[1365.76s] kind of like a highway to your brain.

[1367.44s] So, I think guies are very useful for

[1369.68s] auditing systems and visual

[1371.68s] representations in general. And number

[1373.60s] two, I would say is we have to keep the

[1376.08s] AI on the leash. We I think a lot of

[1378.88s] people are getting way over excited with

[1380.64s] AI agents and uh it's not useful to me

[1383.60s] to get a diff of 10,000 lines of code to

[1385.84s] my repo. Like I have to I'm still the

[1387.92s] bottleneck, right? Even though that

[1389.20s] 10,00 lines come out instantly, I have

[1391.12s] to make sure that this thing is not

[1392.24s] introducing bugs. It's just like and

[1395.36s] that it's doing the correct thing,

[1396.56s] right? And that there's no security

[1397.84s] issues and so on. So um I think that um

[1402.88s] yeah basically you we have to sort of

[1405.44s] like it's in our interest to make the

[1408.24s] the flow of these two go very very fast

[1410.32s] and we have to somehow keep the AI on

[1412.16s] the leash because it gets way too

[1413.12s] overreactive. It's uh it's kind of like

[1415.28s] this. This is how I feel when I do AI

[1417.28s] assisted coding. If I'm just bite coding

[1419.20s] everything is nice and great but if I'm

[1420.88s] actually trying to get work done it's

[1422.40s] not so great to have an overreactive uh

[1424.72s] agent doing all this kind of stuff. So

[1427.28s] this slide is not very good. I'm sorry,

[1428.80s] but I guess I'm trying to develop like

[1431.12s] many of you some ways of utilizing these

[1433.84s] agents in my coding workflow and to do

[1435.76s] AI assisted coding. And in my own work,

[1438.08s] I'm always scared to get way too big

[1439.84s] diffs. I always go in small incremental

[1442.24s] chunks. I want to make sure that

[1444.16s] everything is good. I want to spin this

[1446.16s] loop very very fast and um I sort of

[1449.12s] work on small chunks of single concrete

[1450.80s] thing. Uh and so I think many of you

[1453.20s] probably are developing similar ways of

[1454.64s] working with the with LLMs.

[1457.60s] Um, I also saw a number of blog posts

[1459.60s] that try to develop these best practices

[1462.24s] for working with LLMs. And here's one

[1464.00s] that I read recently and I thought was

[1465.36s] quite good. And it kind of discussed

[1466.80s] some techniques and some of them have to

[1468.24s] do with how you keep the AI on the

[1469.92s] leash. And so, as an example, if you are

[1472.00s] prompting, if your prompt is vague, then

[1474.96s] uh the AI might not do exactly what you

[1476.96s] wanted and in that case, verification

[1478.88s] will fail. You're going to ask for

[1480.24s] something else. If a verification fails,

[1482.08s] then you're going to start spinning. So

[1483.68s] it makes a lot more sense to spend a bit

[1485.12s] more time to be more concrete in your

[1486.80s] prompts which increases the probability

[1488.48s] of successful verification and you can

[1490.24s] move forward. And so I think a lot of us

[1492.08s] are going to end up finding um kind of

[1494.08s] techniques like this. I think in my own

[1496.32s] work as well I'm currently interested in

[1497.84s] uh what education looks like in um

[1500.08s] together with kind of like now that we

[1501.84s] have AI uh and LLMs what does education

[1504.48s] look like? And I think a a large amount

[1507.04s] of thought for me goes into how we keep

[1509.68s] AI on the leash. I don't think it just

[1511.44s] works to go to chat and be like, "Hey,

[1513.20s] teach me physics." I don't think this

[1514.80s] works because the AI is like gets lost

[1516.88s] in the woods. And so for me, this is

[1518.80s] actually two separate apps. For example,

[1520.88s] there's an app for a teacher that

[1522.64s] creates courses and then there's an app

[1524.88s] that takes courses and serves them to

[1526.48s] students. And in both cases, we now have

[1529.12s] this intermediate artifact of a course

[1531.20s] that is auditable and we can make sure

[1532.72s] it's good. We can make sure it's

[1533.84s] consistent. and the AI is kept on the

[1535.92s] leash with respect to a certain

[1537.12s] syllabus, a certain like um progression

[1540.24s] of projects and so on. And so this is

[1542.64s] one way of keeping the AI on leash and I

[1544.16s] think has a much higher likelihood of

[1545.76s] working and the AI is not getting lost

[1547.76s] in the woods.

[1549.92s] One more kind of analogy I wanted to

[1551.92s] sort of allude to is I'm not I'm no

[1554.48s] stranger to partial autonomy and I kind

[1556.16s] of worked on this I think for five years

[1557.84s] at Tesla and this is also a partial

[1560.24s] autonomy product and shares a lot of the

[1561.92s] features like for example right there in

[1563.52s] the instrument panel is the GUI of the

[1565.44s] autopilot so it's showing me what the

[1567.60s] what the neural network sees and so on

[1569.20s] and we have the autonomy slider where

[1570.80s] over the course of my tenure there we

[1573.44s] did more and more autonomous tasks for

[1575.60s] the user and maybe the story that I

[1578.32s] wanted to tell very briefly is uh

[1581.12s] actually the first time I drove a

[1582.64s] self-driving vehicle was in 2013 and I

[1585.20s] had a friend who worked at Whimo and uh

[1587.28s] he offered to give me a drive around

[1589.12s] Palo Alto. I took this picture using

[1591.52s] Google Glass at the time and many of you

[1593.92s] are so young that you might not even

[1595.28s] know what that is. Uh but uh yeah, this

[1597.28s] was like all the rage at the time. And

[1599.44s] we got into this car and we went for

[1600.96s] about a 30-minute drive around Palo Alto

[1602.96s] highways uh streets and so on. And this

[1605.12s] drive was perfect. There was zero

[1606.96s] interventions and this was 2013 which is

[1609.84s] now 12 years ago. And it kind of struck

[1612.48s] me because at the time when I had this

[1614.00s] perfect drive, this perfect demo, I felt

[1616.16s] like, wow, self-driving is imminent

[1619.52s] because this just worked. This is

[1620.80s] incredible. Um, but here we are 12 years

[1623.44s] later and we are still working on

[1624.88s] autonomy. Um, we are still working on

[1627.04s] driving agents and even now we haven't

[1629.20s] actually like really solved the problem.

[1630.80s] like you may see Whimos going around and

[1632.88s] they look driverless but you know

[1634.96s] there's still a lot of teleoperation and

[1636.80s] a lot of human in the loop of a lot of

[1638.72s] this driving so we still haven't even

[1640.96s] like declared success but I think it's

[1642.56s] definitely like going to succeed at this

[1644.40s] point but it just took a long time and

[1646.56s] so I think like like this is software is

[1649.36s] really tricky I think in the same way

[1651.60s] that driving is tricky and so when I see

[1654.72s] things like oh 2025 is the year of

[1656.48s] agents I get very concerned and I kind

[1658.72s] of feel like you know this is the decade

[1661.04s] of agents and this is going to be quite

[1664.08s] some time. We need humans in the loop.

[1665.76s] We need to do this carefully. This is

[1667.20s] software. Let's be serious here. One

[1671.04s] more kind of analogy that I always think

[1672.88s] through is the Iron Man suit. Uh I think

[1676.08s] this is I always love Iron Man. I think

[1678.16s] it's like so um correct in a bunch of

[1681.36s] ways with respect to technology and how

[1682.88s] it will play out. And what I love about

[1684.40s] the Iron Man suit is that it's both an

[1685.92s] augmentation and Tony Stark can drive it

[1688.72s] and it's also an agent. And in some of

[1690.32s] the movies, the Iron Man suit is quite

[1691.84s] autonomous and can fly around and find

[1693.60s] Tony and all this kind of stuff. And so

[1695.28s] this is the autonomy slider is we can be

[1697.28s] we can build augmentations or we can

[1699.04s] build agents and we kind of want to do a

[1701.20s] bit of both. But at this stage I would

[1703.44s] say working with fallible LLMs and so

[1705.92s] on. I would say you know it's less Iron

[1709.12s] Man robots and more Iron Man suits that

[1711.60s] you want to build. It's less like

[1713.68s] building flashy demos of autonomous

[1715.12s] agents and more building partial

[1716.72s] autonomy products. And these products

[1719.68s] have custom gueies and UIUX. And we're

[1721.92s] trying to um and this is done so that

[1723.84s] the generation verification loop of the

[1725.52s] human is very very fast. But we are not

[1728.16s] losing the sight of the fact that it is

[1729.52s] in principle possible to automate this

[1731.28s] work. And there should be an autonomy

[1732.96s] slider in your product. And you should

[1734.56s] be thinking about how you can slide that

[1735.92s] autonomy slider and make your product uh

[1738.56s] sort of um more autonomous over time.

[1741.28s] But this is kind of how I think there's

[1742.72s] lots of opportunities in these kinds of

[1744.24s] products. I want to now switch gears a

[1746.56s] little bit and talk about one other

[1748.16s] dimension that I think is very unique.

[1749.84s] Not only is there a new type of

[1751.44s] programming language that allows for

[1752.96s] autonomy in software but also as I

[1755.28s] mentioned it's programmed in English

[1756.64s] which is this natural interface and

[1759.04s] suddenly everyone is a programmer

[1760.56s] because everyone speaks natural language

[1762.24s] like English. So this is extremely

[1764.64s] bullish and very interesting to me and

[1766.16s] also completely unprecedented. I would

[1768.00s] say it it used to be the case that you

[1769.52s] need to spend five to 10 years studying

[1771.44s] something to be able to do something in

[1772.88s] software. this is not the case anymore.

[1775.20s] So, I don't know if by any chance anyone

[1777.12s] has heard of vibe coding.

[1780.64s] Uh, this this is the tweet that kind of

[1782.48s] like introduced this, but I'm told that

[1784.24s] this is now like a major meme. Um, fun

[1786.72s] story about this is that I've been on

[1789.60s] Twitter for like 15 years or something

[1791.20s] like that at this point and I still have

[1793.52s] no clue which tweet will become viral

[1796.32s] and which tweet like fizzles and no one

[1798.00s] cares. And I thought that this tweet was

[1800.80s] going to be the latter. I don't know. It

[1801.84s] was just like a shower of thoughts. But

[1803.36s] this became like a total meme and I

[1805.28s] really just can't tell. But I guess like

[1806.72s] it struck a chord and it gave a name to

[1808.48s] something that everyone was feeling but

[1810.56s] couldn't quite say in words. So now

[1813.28s] there's a Wikipedia page and everything.

[1817.28s] This is like

[1818.64s] [Applause]

[1825.92s] yeah this is like a major contribution

[1827.60s] now or something like that. So,

[1830.72s] um, so Tom Wolf from HuggingFace shared

[1832.96s] this beautiful video that I really love.

[1834.96s] Um,

[1837.76s] these are kids vibe coding.

[1842.64s] And I find that this is such a wholesome

[1844.40s] video. Like, I love this video. Like,

[1846.72s] how can you look at this video and feel

[1848.08s] bad about the future? The future is

[1849.84s] great.

[1852.56s] I think this will end up being like a

[1853.92s] gateway drug to software development.

[1856.64s] Um, I'm not a doomer about the future of

[1859.20s] the generation and I think yeah, I love

[1862.24s] this video. So, I tried by coding a

[1864.80s] little bit uh as well because it's so

[1867.12s] fun. Uh, so bike coding is so great when

[1869.36s] you want to build something super duper

[1870.80s] custom that doesn't appear to exist and

[1872.40s] you just want to wing it because it's a

[1873.68s] Saturday or something like that. So, I

[1875.52s] built this uh iOS app and I don't I

[1878.72s] can't actually program in Swift, but I

[1880.64s] was really shocked that I was able to

[1881.76s] build like a super basic app and I'm not

[1883.36s] going to explain it. It's really uh

[1884.72s] dumb, but uh I kind of like this was

[1887.36s] just like a day of work and this was

[1888.72s] running on my phone like later that day

[1890.32s] and I was like, "Wow, this is amazing."

[1892.32s] I didn't have to like read through Swift

[1893.92s] for like five days or something like

[1895.92s] that to like get started. I also

[1898.16s] vipcoded this app called Menu Genen. And

[1900.48s] this is live. You can try it in

[1901.76s] menu.app. And I basically had this

[1904.08s] problem where I show up at a restaurant,

[1905.44s] I read through the menu, and I have no

[1906.64s] idea what any of the things are. And I

[1908.56s] need pictures. So this doesn't exist. So

[1911.60s] I was like, "Hey, I'm going to bite code

[1912.96s] it." So, um, this is what it looks like.

[1915.92s] You go to menu.app,

[1918.24s] um, and, uh, you take a picture of a of

[1921.44s] a menu and then menu generates the

[1923.28s] images and everyone gets $5 in credits

[1926.24s] for free when you sign up. And

[1928.00s] therefore, this is a major cost center

[1930.48s] in my life. So, this is a negative

[1933.76s] negative uh, revenue app for me right

[1936.24s] now.

[1937.84s] I've lost a huge amount of money on

[1939.20s] menu.

[1941.28s] Okay. But the fascinating thing about

[1943.36s] menu genen for me is that the code of

[1948.16s] the v the vite coding part the code was

[1950.24s] actually the easy part of v of v coding

[1952.72s] menu and most of it actually was when I

[1955.12s] tried to make it real so that you can

[1956.48s] actually have authentication and

[1957.60s] payments and the domain name and averal

[1959.60s] deployment. This was really hard and all

[1961.92s] of this was not code. All of this devops

[1964.16s] stuff was in me in the browser clicking

[1967.12s] stuff and this was extreme slo and took

[1969.84s] another week. So it was really

[1971.52s] fascinating that I had the menu genen um

[1974.64s] basically demo working on my laptop in a

[1977.28s] few hours and then it took me a week

[1979.28s] because I was trying to make it real and

[1981.20s] the reason for this is this was just

[1982.88s] really annoying. Um, so for example, if

[1985.60s] you try to add Google login to your web

[1987.28s] page, I know this is very small, but

[1989.20s] just a huge amount of instructions of

[1991.68s] this clerk library telling me how to

[1993.60s] integrate this. And this is crazy. Like

[1995.20s] it's telling me go to this URL, click on

[1997.52s] this dropdown, choose this, go to this,

[1999.76s] and click on that. And it's like telling

[2001.20s] me what to do. Like a computer is

[2002.64s] telling me the actions I should be

[2004.88s] taking. Like you do it. Why am I doing

[2006.64s] this?

[2008.64s] What the hell?

[2011.76s] I had to follow all these instructions.

[2013.84s] This was crazy. So I think the last part

[2016.16s] of my talk therefore focuses on can we

[2019.52s] just build for agents? I don't want to

[2021.68s] do this work. Can agents do this? Thank

[2024.24s] you.

[2026.32s] Okay. So roughly speaking, I think

[2028.64s] there's a new category of consumer and

[2030.88s] manipulator of digital information. It

[2033.12s] used to be just humans through GUIs or

[2035.44s] computers through APIs. And now we have

[2037.52s] a completely new thing and agents are

[2040.24s] they're computers but they are humanlike

[2042.80s] kind of right they're people spirits

[2044.32s] there's people spirits on the internet

[2045.60s] and they need to interact with our

[2046.72s] software infrastructure like can we

[2048.32s] build for them it's a new thing so as an

[2050.64s] example you can have robots.txt on your

[2052.96s] domain and you can instruct uh or like

[2055.12s] advise I suppose um uh web crawlers on

[2058.32s] how to behave on your website in the

[2059.84s] same way you can have maybe lm.txt txt

[2061.52s] file which is just a simple markdown

[2063.36s] that's telling LLMs what this domain is

[2065.68s] about and this is very readable to a to

[2068.08s] an LLM. If it had to instead get the

[2070.56s] HTML of your web page and try to parse

[2072.48s] it, this is very errorprone and

[2073.84s] difficult and will screw it up and it's

[2075.68s] not going to work. So we can just

[2076.80s] directly speak to the LLM. It's worth

[2078.40s] it. Um a huge amount of documentation is

[2081.28s] currently written for people. So you

[2082.72s] will see things like lists and bold and

[2085.60s] pictures and this is not directly

[2087.76s] accessible by an LLM. So I see some of

[2091.20s] the services now are transitioning a lot

[2092.80s] of the their docs to be specifically for

[2094.88s] LLMs. So Versell and Stripe as an

[2097.04s] example are early movers here but there

[2099.44s] are a few more that I've seen already

[2101.92s] and they offer their documentation in

[2104.16s] markdown. Markdown is super easy for LMS

[2106.72s] to understand. This is great. Um maybe

[2110.08s] one simple example from from uh my

[2112.32s] experience as well. Maybe some of you

[2114.08s] know three blue one brown. He makes

[2115.60s] beautiful animation videos on YouTube.

[2119.36s] [Applause]

[2123.20s] Yeah, I love this library. So that he

[2125.04s] wrote uh Manon and I wanted to make my

[2127.44s] own and uh there's extensive

[2130.08s] documentations on how to use manon and

[2132.64s] so I didn't want to actually read

[2134.00s] through it. So I copy pasted the whole

[2135.36s] thing to an LLM and I described what I

[2137.44s] wanted and it just worked out of the box

[2139.20s] like LLM just bcoded me an animation

[2141.44s] exactly what I wanted and I was like wow

[2143.28s] this is amazing. So if we can make docs

[2145.84s] legible to LLMs, it's going to unlock a

[2148.16s] huge amount of um kind of use and um I

[2151.20s] think this is wonderful and should

[2152.40s] should happen more. The other thing I

[2155.12s] wanted to point out is that you do

[2156.24s] unfortunately have to it's not just

[2157.68s] about taking your docs and making them

[2158.96s] appear in markdown. That's the easy

[2160.64s] part. We actually have to change the

[2161.92s] docs because anytime your docs say click

[2164.72s] this is bad. An LLM will not be able to

[2166.80s] natively take this action right now. So,

[2169.92s] Verscell, for example, is replacing

[2171.52s] every occurrence of click with an

[2173.52s] equivalent curl command that your LM

[2175.36s] agent could take on your behalf. Um, and

[2178.24s] so I think this is very interesting. And

[2179.76s] then, of course, there's a model context

[2181.36s] protocol from Enthropic. And this is

[2183.04s] also another way, it's a protocol of

[2184.88s] speaking directly to agents as this new

[2186.72s] consumer and manipulator of digital

[2188.16s] information. So, I'm very bullish on

[2189.68s] these ideas. The other thing I really

[2191.52s] like is a number of little tools here

[2193.52s] and there that are helping ingest data

[2196.64s] that in like very LLM friendly formats.

[2198.72s] So for example, when I go to a GitHub

[2200.16s] repo like my nanoGPT repo, I can't feed

[2202.72s] this to an LLM and ask questions about

[2204.32s] it uh because it's you know this is a

[2206.72s] human interface on GitHub. So when you

[2208.88s] just change the URL from GitHub to get

[2210.48s] ingest then uh this will actually

[2212.32s] concatenate all the files into a single

[2214.16s] giant text and it will create a

[2215.92s] directory structure etc. And this is

[2217.52s] ready to be copy pasted into your

[2219.04s] favorite LLM and you can do stuff. Maybe

[2221.52s] even more dramatic example of this is

[2223.44s] deep wiki where it's not just the raw

[2225.44s] content of these files. uh this is from

[2228.64s] Devon but also like they have Devon

[2230.96s] basically do analysis of the GitHub repo

[2232.88s] and Devon basically builds up a whole

[2234.64s] docs uh pages just for your repo and you

[2238.00s] can imagine that this is even more

[2239.84s] helpful to copy paste into your LLM. So

[2242.08s] I love all the little tools that

[2243.44s] basically where you just change the URL

[2244.96s] and it makes something accessible to an

[2246.56s] LLM. So this is all well and great and u

[2249.52s] I think there should be a lot more of

[2250.72s] it. One more note I wanted to make is

[2252.72s] that it is absolutely possible that in

[2255.28s] the future LLMs will be able to this is

[2258.00s] not even future this is today they'll be

[2259.60s] able to go around and they'll be able to

[2260.80s] click stuff and so on but I still think

[2262.64s] it's very worth u basically meeting LLM

[2266.08s] halfway LLM's halfway and making it

[2268.56s] easier for them to access all this

[2269.92s] information uh because this is still

[2271.68s] fairly expensive I would say to use and

[2274.40s] uh a lot more difficult and so I do

[2276.64s] think that lots of software there will

[2278.24s] be a long tail where it won't like adapt

[2280.64s] apps because these are not like live

[2282.16s] player sort of repositories or digital

[2284.48s] infrastructure and we will need these

[2286.24s] tools. Uh but I think for everyone else

[2288.40s] I think it's very worth kind of like

[2289.68s] meeting in some middle point. So I'm

[2291.76s] bullish on both if that makes sense.

[2294.64s] So in summary, what an amazing time to

[2297.12s] get into the industry. We need to

[2298.64s] rewrite a ton of code. A ton of code

[2300.72s] will be written by professionals and by

[2303.04s] coders. These LLMs are kind of like

[2305.60s] utilities, kind of like fabs, but

[2307.52s] they're kind of especially like

[2308.80s] operating systems. But it's so early.

[2310.96s] It's like 1960s of operating systems and

[2314.32s] uh and I think a lot of the analogies

[2316.08s] cross over. Um and these LMS are kind of

[2318.96s] like these fallible uh you know people

[2321.60s] spirits that we have to learn to work

[2323.36s] with. And in order to do that properly,

[2325.60s] we need to adjust our infrastructure

[2327.68s] towards it. So when you're building

[2328.96s] these LLM apps, I describe some of the

[2330.64s] ways of working effectively with these

[2332.80s] LLMs and some of the tools that make

[2334.72s] that uh kind of possible and how you can

[2337.04s] spin this loop very very quickly and

[2339.04s] basically create partial tunneling

[2340.80s] products and then um yeah, a lot of code

[2343.52s] has to also be written for the agents

[2344.88s] more directly. But in any case, going

[2347.20s] back to the Iron Man suit analogy, I

[2349.52s] think what we'll see over the next

[2350.88s] decade roughly is we're going to take

[2352.72s] the slider from left to right. And I'm

[2355.92s] very interesting. It's going to be very

[2357.60s] interesting to see what that looks like.

[2359.36s] And I can't wait to build it with all of

[2361.52s] you. Thank you.
