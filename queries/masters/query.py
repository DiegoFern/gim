{
        "0":Query(
            con="conexion",
            data_con={'database':'company.db'},
            query="""SELECT * 
            FROM employee
            fdsd dfsda
            dsafsd sadfsda
            sadfsd sadfdsaf
            sadfsdaf 
            sdfdsfdsfsd sdfdsafsd
            dsafsdfdsfdsfsd 
            dasfdsfsdfsd sdafsdaf """),
        "1":Node(
            File="codes/filter.py",
            inputs=["0"],
            args=["staff_number>=1"]
            ),
        "2":Node(
            File="codes/join.py",
            inputs=["1","1"],
            args=['fname','fname']
            ),
        "3":Node(
            File="codes/filter.py",
            inputs=["2"],
            args=["staff_number>1"]
            ),}
